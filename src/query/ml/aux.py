from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lpad

selected_columns = [
    "Quarter", "Month", "DayofMonth", "DayOfWeek", "OriginStateName",
    "DestStateName", "CRSDepTime", "CRSArrTime", "CRSElapsedTime", "AirTime",
    "Distance", "TaxiOut", "WheelsOff", "WheelsOn", "TaxiIn", "ArrDel15"
]


def build_train_dataframe(df: DataFrame) -> DataFrame:
    df1 = df.select(selected_columns).dropna() \
        .withColumnRenamed("ArrDel15", "target") \
        .withColumn("CRSDepTime", lpad(col("CRSDepTime").cast("string"), 4, "0").substr(1, 2).cast("int")) \
        .withColumn("CRSArrTime", lpad(col("CRSArrTime").cast("string"), 4, "0").substr(1, 2).cast("int"))

    class_1 = df1.filter(col("target") == 1.0)
    class_0 = df1.filter(col("target") == 0.0)

    undersampled_class_0 = class_0.sample(withReplacement=False, fraction=0.25)
    balanced_df = undersampled_class_0.union(class_1)
    return balanced_df


def evaluate_model_performance(df: DataFrame):
    evaluator = MulticlassClassificationEvaluator(labelCol="target", predictionCol="prediction", metricName="accuracy")
    accuracy = evaluator.evaluate(df)

    confusion_matrix = df.groupBy("target", "prediction").count().sort("target", "prediction").collect()
    matrix_dict = {(row["target"], row["prediction"]): row["count"] for row in confusion_matrix}

    TP = matrix_dict.get((1.0, 1.0), 0)
    TN = matrix_dict.get((0.0, 0.0), 0)
    FP = matrix_dict.get((0.0, 1.0), 0)
    FN = matrix_dict.get((1.0, 0.0), 0)

    confusion_matrix_array = [[TN, FP], [FN, TP]]

    f1_evaluator = MulticlassClassificationEvaluator(labelCol="target", predictionCol="prediction", metricName="f1")
    f1_score = f1_evaluator.evaluate(df)

    precision_evaluator = MulticlassClassificationEvaluator(labelCol="target", predictionCol="prediction",
                                                            metricName="weightedPrecision")
    precision = precision_evaluator.evaluate(df)

    recall_evaluator = MulticlassClassificationEvaluator(labelCol="target", predictionCol="prediction",
                                                         metricName="weightedRecall")
    recall = recall_evaluator.evaluate(df)

    print("Confusion Matrix:")
    print(f"[[{TN}, {FP}],")
    print(f" [{FN}, {TP}]]")
    print(f"Accuracy: {accuracy}")
    print(f"F1-score: {f1_score}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")

    return confusion_matrix_array, accuracy, f1_score, precision, recall
