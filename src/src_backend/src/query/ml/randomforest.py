from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.sql import DataFrame


def train_random_forest_model(df: DataFrame):
    categorical_columns = ["OriginStateName", "DestStateName"]
    numerical_columns = ["Quarter", "Month", "DayofMonth", "DayOfWeek", "CRSDepTime", "CRSArrTime", "AirTime",
                         "CRSElapsedTime",
                         "TaxiOut", "WheelsOff", "WheelsOn", "TaxiIn", "Distance"]

    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

    indexers = {}
    for col in categorical_columns:
        indexer = StringIndexer(inputCol=col, outputCol=f"{col}_index")

        fitted_indexer = indexer.fit(train_df)
        train_df = fitted_indexer.transform(train_df)
        test_df = fitted_indexer.transform(test_df)

        indexers[col] = fitted_indexer

    indexed_columns = [f"{col}_index" for col in categorical_columns]

    assembler_inputs = numerical_columns + indexed_columns
    assembler = VectorAssembler(inputCols=assembler_inputs, outputCol="features")

    rf = RandomForestClassifier(featuresCol="features", labelCol="target", numTrees=50, maxDepth=10, maxBins=55)

    pipeline = Pipeline(stages=[assembler, rf])

    model = pipeline.fit(train_df)

    result_df = model.transform(test_df)

    result_df.select("prediction", "target", "features").show()

    return result_df
