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

UX_DATA_CLICK_SCHEMA = StructType(
    [
        StructField("events", ArrayType(StructType([
            StructField("key", StringType(), True),
            StructField("count", IntegerType(), True),
            StructField("segmentation", StructType([
                StructField("type", StringType(), True),
                StructField("x", IntegerType(), True),
                StructField("y", IntegerType(), True),
                StructField("width", IntegerType(), True),
                StructField("height", IntegerType(), True),
                StructField("parent", StructType([
                    StructField("x", DoubleType(), True),
                    StructField("y", DoubleType(), True),
                    StructField("width", IntegerType(), True),
                    StructField("height", IntegerType(), True)
                ])),
                StructField("domain", StringType(), True),
            ])),
            StructField("timestamp", LongType(), True),
            StructField("hour", IntegerType(), True),
            StructField("dow", IntegerType(), True)
        ]))),
        StructField("app_key", StringType(), True),
        StructField("device_id", StringType(), True),
        StructField("sdk_name", StringType(), True),
        StructField("sdk_version", StringType(), True),
        StructField("t", IntegerType(), True),
        StructField("timestamp", LongType()),
        StructField("hour", IntegerType(), True),
        StructField("dow", IntegerType(), True),
        StructField("raw_html", StringType(), True),
        StructField("screen_size_type", StringType(), True),
        StructField("_id", StringType(), True)
    ]
)

UX_DATA_HEATMAP_MOBILE_IMAGES_SCHEMA = StructType(
    [
        StructField("device_id", StringType(), True),
        StructField("vc_class_name", StringType(), True),
        StructField("screenX", IntegerType(), True),
        StructField("screenY", IntegerType(), True),
        StructField("device_os", StringType(), True),
        StructField("device_model_name", StringType(), True),
        StructField("screen_size", StringType(), True),
        StructField("timestamp", LongType(), True),
        StructField("file_path", StringType(), True),
        StructField("bucket", StringType(), True),
        StructField("_id", StringType())
    ]
)

UX_DATA_HEATMAP_WEB_IMAGES_SCHEMA = StructType(
    [
        StructField("event_id", StringType(), True),
        StructField("bucket", StringType(), True),
        StructField("file_path", StringType(), True),
        StructField("view", StringType(), True),
        StructField("domain", StringType(), True),
        StructField("width", IntegerType(), True),
        StructField("height", IntegerType(), True),
        StructField("screen_size_type", StringType(), True),
        StructField("timestamp", LongType(), True),
        StructField("_id", StringType()),
    ]
)

UX_DATA_INSERT_LOGS_COLLECTION_SCHEMA = StructType(
    [
        StructField("collection", StringType(), True),
        StructField("query", StringType(), True),
        StructField("data", StructType(
            [
                StructField("ts", LongType(), True),
                StructField("reqts", LongType(), True),
                StructField("d", StructType([
                    StructField("id", StringType(), True),
                    StructField("p", StringType(), True),
                    StructField("pv", StringType(), True)
                ])),
                StructField("l", StructType([
                    StructField("cc", StringType(), True),
                    StructField("cty", StringType(), True)
                ])),
                StructField("v", StringType(), True),
                StructField("t", StringType(), True),
                StructField("q", StringType(), True),
                StructField("s", StructType([
                    StructField("version", StringType(), True),
                    StructField("name", StringType(), True)
                ])),
                StructField("h", StructType([
                    StructField("host", StringType(), True),
                    StructField("x-request-id", StringType(), True),
                    StructField("x-real-ip", StringType(), True),
                    StructField("x-forwarded-for", StringType(), True),
                    StructField("x-forwarded-port", StringType(), True),
                    StructField("x-forwarded-proto", StringType(), True),
                    StructField("x-forwarded-scheme", StringType(), True),
                    StructField("x-scheme", StringType(), True),
                    StructField("sec-ch-ua", StringType(), True),
                    StructField("sec-ch-ua-mobile", StringType(), True),
                    StructField("user-agent", StringType(), True),
                    StructField("sec-ch-ua-platform", StringType(), True),
                    StructField("accept", StringType(), True),
                    StructField("origin", StringType(), True),
                    StructField("sec-fetch-site", StringType(), True),
                    StructField("sec-fetch-mode", StringType(), True),
                    StructField("sec-fetch-dest", StringType(), True),
                    StructField("referer", StringType(), True),
                    StructField("accept-encoding", StringType(), True),
                    StructField("accept-language", StringType(), True),
                ]), True),
                StructField("m", StringType(), True),
                StructField("b", BooleanType()),
                StructField("c", BooleanType()),
                StructField("res", StringType(), True),
                StructField("p", BooleanType())
            ]
        ))
    ]
)

UX_DATA_HEATMAP_MOBILE_EVENTS_SCHEMA = StructType(
    [
        StructField("app_key", StringType(), True),
        StructField("device_id", StringType(), True),
        StructField("device_os", StringType(), True),
        StructField("device_model_name", StringType(), True),
        StructField("screenX", StringType(), True),
        StructField("screeenY", StringType(), True),
        StructField("vc_appear_events", 
            ArrayType(
                StructType(
                    [
                        StructField("vc_class_name", StringType(), True),
                        StructField("selector_events", 
                            ArrayType(
                                StructType([
                                    StructField("vc_class_name", StringType(), True),
                                    StructField("selector_name", StringType(), True),
                                    StructField("time", LongType(), True),
                                    StructField("type", StringType(), True),
                                    StructField("view_frame", StructType([
                                        StructField("height", IntegerType(), True),
                                        StructField("width", IntegerType(), True),
                                        StructField("x", IntegerType(), True),
                                        StructField("y", IntegerType(), True),
                                    ]), True),
                                    StructField("instance_class_name", StringType(), True)
                                ])
                            )
                        , True),
                        StructField("multi_touches",
                            ArrayType(
                                StructType([
                                    StructField("time", StringType(), True),
                                    StructField("touches", ArrayType(
                                        StructType([
                                            StructField("id", IntegerType(), True),
                                            StructField("x", IntegerType(), True),
                                            StructField("y", IntegerType(), True)
                                        ])
                                    ) , True),
                                    StructField("type", StringType(), True)
                                ])
                            )            
                        , True),
                        StructField("type", StringType(), True)
                    ]
                )
            )
        , True),
        StructField("screen_size", StringType(), True),
        StructField("_id", StringType(), True)
    ]
)

UX_DATA_SCHEMA_GENNERAL = StructType([
    StructField("collection", StringType(), True),
    StructField("query", StringType(), True),   
    StructField("data", StringType(), True)
])