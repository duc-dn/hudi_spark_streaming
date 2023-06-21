from pyspark.sql.functions import col, from_json, year, month, dayofmonth
from pyspark.sql.dataframe import DataFrame


def parsing_timestamp(df: DataFrame, timestamp_col: str) -> DataFrame:
    """
    parse timestamp following day, month, year
    Args:
        df (DataFrame): DataFrame
        timestamp_col (str): column of timestamp field
        id_col (str): column id which is used to _id of hudi talbe
    Returns:
        DataFrame: return dataframe which adds day, month, year
    """

    # if df has timestamp column, parse it to partition 
    # following day, month, year
    if timestamp_col is not None:
        df = df.withColumn(
            "timestamp",
            (
                col(f"{timestamp_col}") / 1000
            )
            .cast("timestamp")
        )

        df = (
            df
            .withColumn("year", year(df.timestamp))
            .withColumn("month", month(df.timestamp))
            .withColumn("day", dayofmonth(df.timestamp))
        )

    return df.drop("timestamp")