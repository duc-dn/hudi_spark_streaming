from data_config import UX_TABLE_MAPPINGS
from config import HIVE_METASTORE

def get_hoodie_config(topic: str, collection_field: str) -> dict:
    """
    return config of hoodie 
    Args:
        topic (str): topic name

    Returns:
        dict: hoodie options
    """

    hoodie_options = {
        "hoodie.table.name": f'{topic}',
        "hoodie.metadata.enable": "true",
        "hoodie.table.type": "MERGE_ON_READ",
        "hoodie.datasource.write.operation": 
            "UPSERT",
        "hoodie.datasource.write.recordkey.field": 
            UX_TABLE_MAPPINGS[topic]["recordkey_field"],
        "hoodie.datasource.write.partitionpath.field": 
            UX_TABLE_MAPPINGS[topic]["partitionpath_field"],
        'hoodie.datasource.write.table.name': f'{topic}',
        'hoodie.datasource.write.precombine.field': 
            UX_TABLE_MAPPINGS[topic]["precombine"],
        "hoodie.clean.automatic": "true",
        "hoodie.cleaner.policy": "KEEP_LATEST_FILE_VERSIONS",
        "hoodie.cleaner.fileversions.retained": 20,
        "hoodie.compact.inline.max.delta.commits": 3,
        "hoodie.datasource.write.hive_style_partitioning": "true",
        "hoodie.upsert.shuffle.parallelism": "2",
        "hoodie.insert.shuffle.parallelism": "2",
        "hoodie.datasource.hive_sync.enable": "true",
        "hoodie.datasource.hive_sync.mode": "hms",
        "hoodie.datasource.hive_sync.database": "default",
        "hoodie.datasource.hive_sync.table": f"{topic}",
        "hoodie.datasource.hive_sync.partition_fields": 
            UX_TABLE_MAPPINGS[topic]["partitionpath_field"],
        "hoodie.datasource.hive_sync.partition_extractor_class":
            "org.apache.hudi.hive.MultiPartKeysValueExtractor",
        "hoodie.datasource.hive_sync.metastore.uris": HIVE_METASTORE
    }

    return hoodie_options
