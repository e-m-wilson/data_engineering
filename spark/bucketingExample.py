from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Bucketing Example")
    .enableHiveSupport()      # Required for saveAsTable()
    .getOrCreate()
)

# # Optional: make bucketed scans more likely to be used
# spark.conf.set("spark.sql.sources.bucketing.enabled", "true")

# -----------------------------------------------------------------------------
# Sample data
# -----------------------------------------------------------------------------

customers = spark.createDataFrame([
    (1, "Alice"),
    (2, "Bob"),
    (3, "Charlie"),
    (4, "David")
], ["customer_id", "name"])

orders = spark.createDataFrame([
    (101, 1, 125.50),
    (102, 1, 87.00),
    (103, 2, 42.75),
    (104, 4, 199.99)
], ["order_id", "customer_id", "amount"])

# -----------------------------------------------------------------------------
# Write bucketed tables
# -----------------------------------------------------------------------------

customers.write \
    .mode("overwrite") \
    .bucketBy(8, "customer_id") \
    .sortBy("customer_id") \
    .saveAsTable("customers_bucketed")

orders.write \
    .mode("overwrite") \
    .bucketBy(8, "customer_id") \
    .sortBy("customer_id") \
    .saveAsTable("orders_bucketed")

# -----------------------------------------------------------------------------
# Read the tables
# -----------------------------------------------------------------------------

customers_bucketed = spark.table("customers_bucketed")
orders_bucketed = spark.table("orders_bucketed")

# -----------------------------------------------------------------------------
# Join on the bucket column
# -----------------------------------------------------------------------------

joined = (
    customers_bucketed
    .join(orders_bucketed, on="customer_id")
)

joined.show()

# -----------------------------------------------------------------------------
# Inspect the physical plan
# -----------------------------------------------------------------------------

joined.explain(True)