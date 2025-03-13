"""main.py"""
from pyspark.sql import SparkSession

def etl_process(input_path, output_path):
    spark = SparkSession.builder \
        .master('spark://spark:7077') \
        .appName("SimpleApp") \
        .getOrCreate()

    data = spark.read.csv(input_path, header=True, inferSchema=True)

    selected_columns = [
        "Year", "Quarter", "Month", "DayofMonth", "DayOfWeek", "FlightDate", 
        "Reporting_Airline", "DOT_ID_Reporting_Airline", "IATA_CODE_Reporting_Airline", 
        "Tail_Number", "Flight_Number_Reporting_Airline", "OriginAirportID", 
        "OriginAirportSeqID", "OriginCityMarketID", "Origin", "OriginCityName", 
        "OriginState", "OriginStateFips", "OriginStateName", "OriginWac", 
        "DestAirportID", "DestAirportSeqID", "DestCityMarketID", "Dest", 
        "DestCityName", "DestState", "DestStateFips", "DestStateName", "DestWac", 
        "CRSDepTime", "DepTime", "DepDelay", "DepDelayMinutes", "DepDel15", 
        "DepartureDelayGroups", "DepTimeBlk", "TaxiOut", "WheelsOff", "WheelsOn", 
        "TaxiIn", "CRSArrTime", "ArrTime", "ArrDelay", "ArrDelayMinutes", 
        "ArrDel15", "ArrivalDelayGroups", "ArrTimeBlk", "Cancelled", 
        "CancellationCode", "Diverted", "CRSElapsedTime", "ActualElapsedTime", 
        "AirTime", "Flights", "Distance", "DistanceGroup", "CarrierDelay", 
        "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay", 
        "FirstDepTime", "TotalAddGTime", "LongestAddGTime", "DivAirportLandings", 
        "DivReachedDest", "DivActualElapsedTime", "DivArrDelay", "DivDistance", 
        "Div1Airport", "Div1AirportID", "Div1AirportSeqID", "Div1WheelsOn", 
        "Div1TotalGTime", "Div1LongestGTime", "Div1WheelsOff", "Div1TailNum", 
        "Div2Airport", "Div2AirportID", "Div2AirportSeqID", "Div2WheelsOn", 
        "Div2TotalGTime", "Div2LongestGTime", "Div2WheelsOff", "Div2TailNum", 
        "Div3Airport", "Div3AirportID", "Div3AirportSeqID", "Div3WheelsOn", 
        "Div3TotalGTime", "Div3LongestGTime", "Div3WheelsOff", "Div3TailNum", 
        "Div4Airport", "Div4AirportID", "Div4AirportSeqID", "Div4WheelsOn", 
        "Div4TotalGTime", "Div4LongestGTime", "Div4WheelsOff", "Div4TailNum", 
        "Div5Airport", "Div5AirportID", "Div5AirportSeqID", "Div5WheelsOn", 
        "Div5TotalGTime", "Div5LongestGTime", "Div5WheelsOff", "Div5TailNum"
    ]
    transformed_data = data.select(*selected_columns)

    transformed_data.write.parquet(output_path)

    spark.stop()

if __name__ == "__main__":
    input_path = "/opt/bitnami/spark/datasets/On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)_2013_6.csv"
    output_path = "/opt/bitnami/spark/outputs/transformed_data.parquet"
    etl_process(input_path, output_path)