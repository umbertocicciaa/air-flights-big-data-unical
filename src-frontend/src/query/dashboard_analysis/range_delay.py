from typing import List
from pyspark.sql import DataFrame


def calculateFlightDelays(df : DataFrame)-> List:
    delay = df.filter(df["Cancelled"] == 0).filter(df["Diverted"] == 0).filter(df["ArrDelayMinutes"] > 0)
    range_0_15 = delay.filter(delay["ArrivalDelayGroups"] == 0).count()
    range_15_30 = delay.filter(delay["ArrivalDelayGroups"] == 1).count()
    range_30_45 = delay.filter(delay["ArrivalDelayGroups"] == 2).count()
    range_45_60 = delay.filter(delay["ArrivalDelayGroups"] == 3).count()
    range_over_60 = delay.filter(delay["ArrivalDelayGroups"] > 3).count()
    return [range_0_15,range_15_30,range_30_45,range_45_60,range_over_60]

def calculateFlightDelayRange(df : DataFrame)-> List:
    ris = calculateFlightDelays(df)
    return ris
