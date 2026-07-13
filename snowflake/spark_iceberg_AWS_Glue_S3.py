from pyspark.sql import SparkSession


spark = (
    SparkSession.builder
    .appName("TitanicToIceberg")

    # Iceberg Spark extensions
    .config(
        "spark.sql.extensions",
        "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions"
    )

    # Tell Spark to use AWS Glue as the catalog
    .config(
        "spark.sql.catalog.glue_catalog",
        "org.apache.iceberg.spark.SparkCatalog"
    )
    .config(
        "spark.sql.catalog.glue_catalog.catalog-impl",
        "org.apache.iceberg.aws.glue.GlueCatalog"
    )
    .config(
        "spark.sql.catalog.glue_catalog.warehouse",
        "s3://rev-spark-454497087304-us-east-2-an/iceberg/"
    )
    .config(
        "spark.sql.catalog.glue_catalog.io-impl",
        "org.apache.iceberg.aws.s3.S3FileIO"
    )

    .getOrCreate()
)

titanic_df = spark.read.parquet(
    "s3://rev-spark-454497087304-us-east-2-an/titanic.parquet"
)

titanic_df.printSchema()

spark.sql("""
CREATE DATABASE IF NOT EXISTS glue_catalog.iceberg_demo
""")

(
    titanic_df.writeTo(
        "glue_catalog.iceberg_demo.titanic"
    )
    .using("iceberg")
    .createOrReplace()
)

spark.sql("""
SELECT *
FROM glue_catalog.iceberg_demo.titanic
LIMIT 10
""").show()

spark.stop()