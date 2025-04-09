from pyspark.sql.functions import to_timestamp, lpad, col

def preprocess_data(df):
    selected_columns = ["Year","Quarter","Month","DayofMonth","DayOfWeek","FlightDate","Reporting_Airline","Tail_Number","Flight_Number_Reporting_Airline", "OriginAirportID","Origin","OriginCityName","OriginStateName","DestAirportID" ,"Dest","DestCityName","DestStateName","CRSDepTime","DepTime","DepDelay","CRSArrTime" ,"ArrTime","ArrDelay","Cancelled","CRSElapsedTime","ActualElapsedTime" ,"AirTime","Flights","Distance"]
    df = df.withColumn("CRSDepTime", to_timestamp(lpad(col("CRSDepTime").cast("string"), 4, "0"), "HHmm"))
    df = df.withColumn("DepTime", to_timestamp(lpad(col("DepTime").cast("string"), 4, "0"), "HHmm"))
    df = df.withColumn("CRSArrTime", to_timestamp(lpad(col("CRSArrTime").cast("string"), 4, "0"), "HHmm"))
    df = df.withColumn("ArrTime", to_timestamp(lpad(col("ArrTime").cast("string"), 4, "0"), "HHmm"))
    df_processed = df.select(*selected_columns)
    return df_processed