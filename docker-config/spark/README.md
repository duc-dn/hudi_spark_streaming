```
df = spark.read.format("delta").load("s3a://datalake/demo")

df.createOrReplaceTempView("demo")
```

```
spark = (
            SparkSession.builder.master("local[*]")
            .appName("spark application")
            .config(
                "spark.jars.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,"
                "org.apache.kafka:kafka-clients:2.6.0,"
                "org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.1.1,"
                "org.apache.commons:commons-pool2:2.6.2,"
                "org.apache.spark:spark-avro_2.12:3.1.1,"
                "org.apache.hadoop:hadoop-aws:3.2.0,"
                "com.amazonaws:aws-java-sdk-bundle:1.11.375,"
                "org.apache.hudi:hudi-spark3.1-bundle_2.12:0.11.0"
            )
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
```
