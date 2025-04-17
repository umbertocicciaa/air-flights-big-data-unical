from datetime import datetime
import pandas as pd
from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from services.data_visualization import create_month_dataframe, create_all_dataframe
from query.ml.clustering import clustering_flights_onTime_delayed
from query.ml.aux import build_train_dataframe
from query.airports_analysis.city_fligth_airport import city_flight_airport
from query.airports_analysis.max_frequent_airport_dest import destinations_number_city
from query.airports_analysis.fligth_numbers import calculate_departure_arrival_counts
from query.airports_analysis.flitgh_delays import average_month_delay_for_city
from query.dashboard_analysis.fligth_infos import monthly_flight_statistics
from query.route.find_flight import get_flight
from query.annual_stats.airport_traffic import most_traffic_city
from query.annual_stats.month_week_fligth import get_weekly_flight_counts
from services.session_spark import create_session
from utils.preprocesing import preprocess_data


spark_session=create_session()

def build_month_dataframe(mese:int):
    return create_month_dataframe(spark_session,mese)

def build_all_dataframe():
    return create_all_dataframe(spark_session)

def query_numero_partenze_e_arrivi_citta(citta:str):
    return calculate_departure_arrival_counts(build_all_dataframe(), citta)


def query_ritardo_medio_partenza_arrivo_citta(citta:str) ->list[list[float]]:
    ritardi_medi = [[], []]
    for i in range(1, 13):
        df= build_month_dataframe(i)
        df_mese_from_city = df.filter((df["OriginCityName"] == citta))
        df_mese_to_city = df.filter((df["DestCityName"] == citta))

        ritardi_medi[0].append(average_month_delay_for_city(df_mese_from_city))
        ritardi_medi[1].append(average_month_delay_for_city(df_mese_to_city))

    return ritardi_medi

def query_destinazione_numvoli_citta(aeroporto:str):
    return destinations_number_city(build_all_dataframe(), aeroporto)


def query_citta_numvoli_aeroporto(citta: str):
    return city_flight_airport(build_all_dataframe(),citta)


def query_get_volo(data: datetime.date, origine: str, destinazione: str, ora : datetime.time):
    return get_flight(preprocess_data(build_all_dataframe()),data,origine,destinazione,ora)

def query_mesi_stato_voli():
    numero_stato_voli = [[], [], [], []]
    for i in range(1, 13):
        df = build_month_dataframe(i)
        stato_voli_mese= monthly_flight_statistics(df)
        numero_stato_voli[0].append(stato_voli_mese[0])
        numero_stato_voli[1].append(stato_voli_mese[1])
        numero_stato_voli[2].append(stato_voli_mese[2])
        numero_stato_voli[3].append(stato_voli_mese[3])
    return numero_stato_voli

def query_mesi_voli_settimana():
    NUM_GIORNI_SETTIMANA = 7
    giorni_settimana_numvoli = [[] for i in range(NUM_GIORNI_SETTIMANA)]

    for i in range(1, 13):
        df = build_month_dataframe(i)
        lista_numvoli_settimana = get_weekly_flight_counts(df)

        for j in range(NUM_GIORNI_SETTIMANA):
            giorni_settimana_numvoli[j].append(lista_numvoli_settimana[j])

    return giorni_settimana_numvoli


def query_citta_num_voli() -> pd.DataFrame:
    return most_traffic_city(build_all_dataframe())

def preprocessing_for_classification() -> DataFrame:
    return build_train_dataframe(build_all_dataframe())


columns = ["DepDelay", "ArrDelay", "flight_duration"]
columns_clustering = ["DepDelay", "ArrDelay"]

def preprocessing_clustering(df:DataFrame)->DataFrame:
    df_new = df.filter(
        (col("Cancelled") == 0) &
        (col("Diverted") == 0)
    )
    df_new = df_new.withColumn("flight_duration", df["AirTime"] + df["ArrDelay"])
    df_clustering = df_new.select(columns)

    return df_clustering

def clusteringFlights(df:DataFrame,numCluster:int):
    return clustering_flights_onTime_delayed(df,numCluster,columns, columns_clustering)




