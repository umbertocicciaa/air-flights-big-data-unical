from pyspark.sql import DataFrame
from pyspark.sql.functions import to_timestamp, lpad, col
from query.airports_analysis.city_fligth_airport import city_flight_airport
from query.airports_analysis.fligth_numbers import calculate_departure_arrival_counts
from query.airports_analysis.flitgh_delays import average_month_delay_for_city
from query.airports_analysis.max_frequent_airport_dest import destinations_number_city
from query.annual_stats.airport_traffic import most_traffic_city
from query.annual_stats.month_week_fligth import get_weekly_flight_counts
from query.dashboard_analysis.fligth_infos import monthly_flight_statistics
from query.ml.aux import build_train_dataframe
from query.ml.clustering import clustering_flights_on_time_delayed
from query.route.find_flight import get_flight
from utils.data_visualization import create_month_dataframe, create_all_dataframe
from utils.session_spark import create_session

spark_session = create_session()


def build_month_dataframe(mese: int):
    return create_month_dataframe(mese)


def build_all_dataframe():
    return create_all_dataframe()


def query_numero_partenze_e_arrivi_citta(citta : str):
    return calculate_departure_arrival_counts(build_all_dataframe(), citta)


def query_ritardo_medio_partenza_arrivo_citta(citta : str):
    ritardi_medi = [[], []]
    for i in range(0, 12):
        df = build_month_dataframe(i)
        df_mese_from_city = df.filter((df["OriginCityName"] == citta))
        df_mese_to_city = df.filter((df["DestCityName"] == citta))

        ritardi_medi[0].append(average_month_delay_for_city(df_mese_from_city))
        ritardi_medi[1].append(average_month_delay_for_city(df_mese_to_city))

    return ritardi_medi


def query_destinazione_numvoli_citta(aeroporto : str):
    return destinations_number_city(build_all_dataframe(), aeroporto)


def query_citta_numvoli_aeroporto(citta : str):
    return city_flight_airport(build_all_dataframe(), citta)


def query_get_volo(data, origine, destinazione, ora):
    return get_flight(build_all_dataframe(),data,origine,destinazione,ora)


def query_mesi_stato_voli():
    numero_stato_voli = [[], [], [], []]
    for i in range(0, 12):
        df = build_month_dataframe(i)
        stato_voli_mese = monthly_flight_statistics(df)
        numero_stato_voli[0].append(stato_voli_mese[0])
        numero_stato_voli[1].append(stato_voli_mese[1])
        numero_stato_voli[2].append(stato_voli_mese[2])
        numero_stato_voli[3].append(stato_voli_mese[3])
    return numero_stato_voli


def query_mesi_voli_settimana():
    num_giorni_settimana = 7
    giorni_settimana_numvoli = [[] for _ in range(num_giorni_settimana)]

    for i in range(0, 12):
        df = build_month_dataframe(i)
        lista_numvoli_settimana = get_weekly_flight_counts(df)

        for j in range(num_giorni_settimana):
            giorni_settimana_numvoli[j].append(lista_numvoli_settimana[j])

    return giorni_settimana_numvoli


def query_citta_num_voli():
    return most_traffic_city(build_all_dataframe())


def preprocessing_for_classification():
    return build_train_dataframe(build_all_dataframe())


columns = ["DepDelay", "ArrDelay", "flight_duration"]
columns_clustering = ["DepDelay", "ArrDelay"]


def preprocessing_clustering(df):
    df_new = df.filter(
        (col("Cancelled") == 0) &
        (col("Diverted") == 0)
    )
    df_new = df_new.withColumn("flight_duration", df["AirTime"] + df["ArrDelay"])
    df_clustering = df_new.select(columns)

    return df_clustering


def clustering_flights(df: DataFrame, num_cluster: int):
    return clustering_flights_on_time_delayed(df, num_cluster, columns, columns_clustering)
