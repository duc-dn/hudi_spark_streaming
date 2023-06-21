import logging

from pyspark.sql.functions import col, from_json
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import StringType
from pyspark.sql.streaming import DataStreamReader, StreamingQuery
from pyspark.sql.utils import AnalysisException

from utils.logger import logger
from utils.parser_timestamp import parsing_timestamp
from hoodie_config import get_hoodie_config

from config import (
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_SERVER_HOST,
    KAFKA_BOOTSTRAP_SERVERS
)

from data_config import (
    UX_TABLE_MAPPINGS
)

from schema.ux_schema import (
    UX_DATA_SCHEMA_GENNERAL
)


class HudiSink:
    """
    Ingest data from topic ux_data to MINIO
    """

    def __init__(self) -> None:
        self.spark = (
            SparkSession.builder.master("local[*]")
            .appName("spark application")
            .config(
                "spark.jars.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,"
                "org.apache.kafka:kafka-clients:2.6.0,"
                "org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.1.1,"
                "org.apache.commons:commons-pool2:2.6.2,"
                "org.apache.spark:spark-avro_2.12:3.1.1,"
                "org.apache.hadoop:hadoop-aws:3.1.1,"
                "com.amazonaws:aws-java-sdk:1.11.271,"
                "org.apache.hudi:hudi-spark3.1-bundle_2.12:0.11.0,"
                "org.apache.hudi:hudi-hive-sync:0.11.0"
            )   
            .config("spark.driver.memory", "4g")
            .config("spark.sql.extensions", "org.apache.spark.sql.hudi.HoodieSparkSessionExtension")
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
            .config("spark.hadoop.fs.s3a.impl",
                    "org.apache.hadoop.fs.s3a.S3AFileSystem")
            .config("spark.hadoop.fs.s3a.access.key", MINIO_ACCESS_KEY)
            .config("spark.hadoop.fs.s3a.secret.key", MINIO_SECRET_KEY)
            .config("spark.hadoop.fs.s3a.endpoint", MINIO_SERVER_HOST)
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
            .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
            .config('spark.hadoop.fs.s3a.aws.credentials.provider',
                    'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
            .config("spark.hadoop.fs.s3a.connection.maximum", "1000")
            .getOrCreate()
        )

        self._spark_sc = self.spark.sparkContext
        self._spark_sc.setLogLevel('ERROR')
        self.kafka_bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS
        self.checkpoint_location = "s3a://datalake/checkpoint/"
        self.ux_table_mappings = UX_TABLE_MAPPINGS

    def foreach_batch_function_incremental(self, df: DataFrame, epoch_id: int) -> None:
        """
        Handle each batch when ingesting incremental

        :param df:
        :param epoch_id:
        :return: None
        """

        if df.count() > 0: topic = df.select("topic").first()[0]
        logger.info(f'Epoch_id: {epoch_id} of topic: {topic} is being ingested')

        df = (
            df.select(
                col("value").cast(StringType())
            )
            .select(
                from_json(
                    col("value"), 
                    schema=self.ux_table_mappings[topic]["schema"]
                )
                .alias("value")
            )
            .select("value.*")
        )


        #parsing timestamp field
        df = parsing_timestamp(
            df, 
            self.ux_table_mappings[topic]["timestamp"]
        ) 

        df.show()
        
        # save data to minio
        self.save_to_minio(df, topic=topic, collection_field=None)
        

        # try:
        #     hoodie_options = get_hoodie_config(topic=topic, collection_field=None)
        #     df.write \
        #     .mode("append") \
        #     .format("hudi") \
        #     .options(**hoodie_options) \
        #     .save(path="s3a://datalake/hudi-table")
        # except Exception as e:
        #     logger.error(e)

    def get_data_stream_reader(
            self, topic_name: str, starting_offsets: str = "earliest"
    ) -> DataStreamReader:
        """
        Reading streaming from kafka topic
        :param topic_name:
        :param starting_offsets:
        :return: stream DataFrame
        """
        kafka_bootstrap_servers = self.kafka_bootstrap_servers

        return (
            self.spark.readStream.format("kafka")
                .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
                .option("subscribe", topic_name)
                .option("startingOffsets", starting_offsets)
                .option("groupIdPrefix", f'spark-kafka-source-{topic_name}')
        )

    def ingest_mutiple_topic(self) -> None:
        """
        Ingest ux data from mutiple kafka topic
        :return: None
        """

        for topic in self.ux_table_mappings.keys():
            logger.info(f"Starting ingest topic {topic}")
            df: DataFrame = self.get_data_stream_reader(
                topic
            ).load()

            df: DataFrame = (
                df.select(
                    "topic",
                    "value"
                )
            )

            stream: StreamingQuery = (
                df.writeStream.foreachBatch(
                    self.foreach_batch_function_incremental
                )
                .trigger(processingTime="120 seconds")
                # .option("checkpointLocation", f"s3a://datalake/checkpoint/{topic}")
                .start()
            )
        self.spark.streams.awaitAnyTermination()

    @staticmethod
    def save_to_minio(df, topic, collection_field):
        hoodie_options = get_hoodie_config(topic=topic, collection_field=collection_field)

        if collection_field is not None:
            path = f's3a://datalake/{collection_field}'
        else:
            path = f's3a://datalake/{topic}'

        try:
            df.write \
            .mode("append") \
            .format("hudi") \
            .options(**hoodie_options) \
            .save(path=path)
        except Exception as e:
            logger.error(e)
            
    def run(self) -> None:
        try:
            self.ingest_mutiple_topic()
        except AnalysisException as e:
            logger.error(f'Error: {e}')

if __name__ == "__main__":
    HudiSink().run()
