from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Learning")
    .master("local[*]")
    .getOrCreate()
)

df = spark.createDataFrame(
    [("Alice", 30), ("Bob", 25)],
    ["name", "age"]
)

df.show()

spark.stop()