from schema.cdc_schema import (
    USER_SCHEMA
)

class UxTableMapping():
    def __init__(
            self, 
            schema,
            partitionpath_field: str = 'year,month,day', 
            recordkey_field: str = '_id', 
            precombine: str = 'timestamp',
            timestamp: str = 'data.timestamp',
            operaton: str = "UPSERT",
            id_col: str = 'data._id'
        ) -> None:

        self.partitionpath_field = partitionpath_field
        self.recordkey_field = recordkey_field
        self.precombine = precombine
        self.schema = schema
        self.operation = operaton
        self.timestamp = timestamp
        self.id_col = id_col

    def get_table_config(self):
        return {
            "partitionpath_field": self.partitionpath_field,
            "recordkey_field": self.recordkey_field,
            "precombine": self.precombine,
            "schema": self.schema,
            "operation": self.operation,
            "timestamp": self.timestamp,
            "id_col": self.id_col
        }

# create hoodie config for each table 
UX_TABLE_MAPPINGS = {
    "cdc__test_user": 
        UxTableMapping(
            schema=USER_SCHEMA,
            timestamp="_airbyte_emitted_at",
            precombine="_airbyte_emitted_at",
            recordkey_field="_airbyte_data.user_id"
        )
        .get_table_config()
}

