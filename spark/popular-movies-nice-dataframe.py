from pyspark.sql import SparkSession
from pyspark.sql import functions as func
from pyspark.sql.types import StructType, StructField, IntegerType, LongType, StringType
from pyspark.sql.functions import udf

def loadMovieNames() -> dict[int, str]:
    movieNames = {}
    # CHANGE THIS TO THE PATH TO YOUR u.ITEM FILE:
    with open("./ml-100k/u.item", "r", encoding='ISO-8859-1', errors='ignore') as f:
        for line in f:
            fields = line.split('|')
            movieNames[int(fields[0])] = fields[1]
    return movieNames

spark = SparkSession.builder.appName("PopularMovies").getOrCreate()
spark.sparkContext.setLogLevel('WARN')

nameDict = spark.sparkContext.broadcast(loadMovieNames())

# Create schema when reading u.data
schema = StructType([ \
                     StructField("userID", IntegerType()), \
                     StructField("movieID", IntegerType()), \
                     StructField("rating", IntegerType()), \
                     StructField("timestamp", LongType())])

# Load up movie data as dataframe
moviesDF = spark.read.option("sep", "\t").schema(schema).csv("./ml-100k/u.data")

movieCounts = moviesDF.groupBy("movieID").count()

# Create a user-defined function to look up movie names from our broadcasted dictionary
# this supports older spark verions:
# def lookupName(movieID: int) -> str:
#     return nameDict.value.get(movieID, "Unknown")

# lookupNameUDF = func.udf(lookupName, StringType())
# MODERN WAY:
@udf
def lookupName(movieID: int) -> str:
    return nameDict.value.get(movieID, "Unknown")

# Add a movieTitle column using our new udf
moviesWithNames = movieCounts.withColumn("movieTitle", lookupName(func.col("movieID")))

# Sort the results
sortedMoviesWithNames = moviesWithNames.orderBy(func.desc("count"))

# Grab the top 10
sortedMoviesWithNames.show(10, False)

# Stop the session
spark.stop()