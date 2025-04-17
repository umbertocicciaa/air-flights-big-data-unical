
from pyspark.sql import DataFrame


def get_weekly_flight_counts(df:DataFrame):
    fligths = (df.groupby("DayOfWeek").count()).sort("DayOfWeek")
    return [row["count"] for row in fligths.collect()]