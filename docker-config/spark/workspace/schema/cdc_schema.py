from pyspark.sql.types import (
    StringType,
    IntegerType,
    StructType,
    StructField,
    LongType, 
    ArrayType,
    DoubleType,
    BooleanType
)


USER_SCHEMA = StructType([
    StructField("_airbyte_ab_id", StringType(), False),
    StructField("_airbyte_stream", StringType(), False),
    StructField("_airbyte_emitted_at", LongType(), False),
    StructField("_airbyte_data", StructType([
        StructField("user_id", StringType(), False),
        StructField("username", StringType(), True),
        StructField("created_at", StringType(), False),
        StructField("_ab_cdc_updated_at", StringType(), False),
        StructField("_ab_cdc_lsn", IntegerType(), False),
        StructField("_ab_cdc_deleted_at", StringType(), True)
    ]))
])