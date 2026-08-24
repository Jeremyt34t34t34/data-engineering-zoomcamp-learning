# Databricks notebook source
# MAGIC %md
# MAGIC # 02 - Build Silver
# MAGIC
# MAGIC Silver tables clean, standardize, and union the raw taxi sources.
# MAGIC
# MAGIC This mirrors the Module 4 dbt staging + intermediate layers:
# MAGIC
# MAGIC ```text
# MAGIC stg_yellow_tripdata
# MAGIC stg_green_tripdata
# MAGIC int_trips_unioned
# MAGIC int_trips
# MAGIC ```

# COMMAND ----------

from pyspark.sql import functions as F

dbutils.widgets.text("catalog", "hive_metastore")

catalog = dbutils.widgets.get("catalog")
bronze = f"`{catalog}`.`bronze`"
silver = f"`{catalog}`.`silver`"

# COMMAND ----------

yellow_raw = spark.table(f"{bronze}.`yellow_taxi_trips_raw`")
green_raw = spark.table(f"{bronze}.`green_taxi_trips_raw`")
zones_raw = spark.table(f"{bronze}.`taxi_zones_raw`")

# COMMAND ----------

yellow_cleaned = (
    yellow_raw
    .where(F.col("VendorID").isNotNull())
    .select(
        F.col("VendorID").cast("int").alias("vendor_id"),
        F.col("RatecodeID").cast("int").alias("rate_code_id"),
        F.col("PULocationID").cast("int").alias("pickup_location_id"),
        F.col("DOLocationID").cast("int").alias("dropoff_location_id"),
        F.col("tpep_pickup_datetime").cast("timestamp").alias("pickup_datetime"),
        F.col("tpep_dropoff_datetime").cast("timestamp").alias("dropoff_datetime"),
        F.col("store_and_fwd_flag").cast("string").alias("store_and_fwd_flag"),
        F.col("passenger_count").cast("int").alias("passenger_count"),
        F.col("trip_distance").cast("double").alias("trip_distance"),
        F.lit(1).cast("int").alias("trip_type"),
        F.col("fare_amount").cast("double").alias("fare_amount"),
        F.col("extra").cast("double").alias("extra"),
        F.col("mta_tax").cast("double").alias("mta_tax"),
        F.col("tip_amount").cast("double").alias("tip_amount"),
        F.col("tolls_amount").cast("double").alias("tolls_amount"),
        F.lit(0.0).cast("double").alias("ehail_fee"),
        F.col("improvement_surcharge").cast("double").alias("improvement_surcharge"),
        F.col("total_amount").cast("double").alias("total_amount"),
        F.col("payment_type").cast("int").alias("payment_type"),
        F.lit("Yellow").alias("service_type"),
    )
)

green_cleaned = (
    green_raw
    .where(F.col("VendorID").isNotNull())
    .select(
        F.col("VendorID").cast("int").alias("vendor_id"),
        F.col("RatecodeID").cast("int").alias("rate_code_id"),
        F.col("PULocationID").cast("int").alias("pickup_location_id"),
        F.col("DOLocationID").cast("int").alias("dropoff_location_id"),
        F.col("lpep_pickup_datetime").cast("timestamp").alias("pickup_datetime"),
        F.col("lpep_dropoff_datetime").cast("timestamp").alias("dropoff_datetime"),
        F.col("store_and_fwd_flag").cast("string").alias("store_and_fwd_flag"),
        F.col("passenger_count").cast("int").alias("passenger_count"),
        F.col("trip_distance").cast("double").alias("trip_distance"),
        F.col("trip_type").cast("int").alias("trip_type"),
        F.col("fare_amount").cast("double").alias("fare_amount"),
        F.col("extra").cast("double").alias("extra"),
        F.col("mta_tax").cast("double").alias("mta_tax"),
        F.col("tip_amount").cast("double").alias("tip_amount"),
        F.col("tolls_amount").cast("double").alias("tolls_amount"),
        F.col("ehail_fee").cast("double").alias("ehail_fee"),
        F.col("improvement_surcharge").cast("double").alias("improvement_surcharge"),
        F.col("total_amount").cast("double").alias("total_amount"),
        F.col("payment_type").cast("int").alias("payment_type"),
        F.lit("Green").alias("service_type"),
    )
)

zones = (
    zones_raw
    .select(
        F.col("LocationID").cast("int").alias("location_id"),
        F.col("Borough").cast("string").alias("borough"),
        F.col("Zone").cast("string").alias("zone"),
        F.col("service_zone").cast("string").alias("service_zone"),
    )
)

# COMMAND ----------

trips_unioned = green_cleaned.unionByName(yellow_cleaned)

trips = (
    trips_unioned
    .where(F.col("pickup_datetime").isNotNull())
    .where(F.col("dropoff_datetime").isNotNull())
    .where(F.col("dropoff_datetime") > F.col("pickup_datetime"))
    .where(F.col("total_amount") >= 0)
    .withColumn(
        "trip_id",
        F.sha2(
            F.concat_ws(
                "||",
                F.coalesce(F.col("vendor_id").cast("string"), F.lit("")),
                F.coalesce(F.col("pickup_datetime").cast("string"), F.lit("")),
                F.coalesce(F.col("pickup_location_id").cast("string"), F.lit("")),
                F.coalesce(F.col("service_type"), F.lit("")),
            ),
            256,
        ),
    )
    .withColumn(
        "trip_duration_minutes",
        (F.col("dropoff_datetime").cast("long") - F.col("pickup_datetime").cast("long")) / 60.0,
    )
    .dropDuplicates(["trip_id"])
)

# COMMAND ----------

yellow_cleaned.write.format("delta").mode("overwrite").option("overwriteSchema", True).saveAsTable(
    f"{silver}.`yellow_taxi_trips_cleaned`"
)

green_cleaned.write.format("delta").mode("overwrite").option("overwriteSchema", True).saveAsTable(
    f"{silver}.`green_taxi_trips_cleaned`"
)

zones.write.format("delta").mode("overwrite").option("overwriteSchema", True).saveAsTable(
    f"{silver}.`taxi_zones`"
)

trips.write.format("delta").mode("overwrite").option("overwriteSchema", True).saveAsTable(
    f"{silver}.`taxi_trips`"
)

# COMMAND ----------

display(spark.sql(f"""
SELECT service_type, COUNT(*) AS trips, ROUND(SUM(total_amount), 2) AS total_amount
FROM {silver}.`taxi_trips`
GROUP BY service_type
ORDER BY service_type
"""))
