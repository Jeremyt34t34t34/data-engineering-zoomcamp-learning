# Databricks notebook source
# MAGIC %md
# MAGIC # 03 - Build Gold
# MAGIC
# MAGIC Gold tables are business-facing analytics tables.
# MAGIC
# MAGIC This mirrors the dbt marts layer.

# COMMAND ----------

from pyspark.sql import functions as F

dbutils.widgets.text("catalog", "hive_metastore")

catalog = dbutils.widgets.get("catalog")
silver = f"`{catalog}`.`silver`"
gold = f"`{catalog}`.`gold`"

# COMMAND ----------

trips = spark.table(f"{silver}.`taxi_trips`")
zones = spark.table(f"{silver}.`taxi_zones`")

pickup_zones = (
    zones
    .select(
        F.col("location_id").alias("pickup_location_id"),
        F.col("borough").alias("pickup_borough"),
        F.col("zone").alias("pickup_zone"),
        F.col("service_zone").alias("pickup_service_zone"),
    )
)

trips_enriched = trips.join(pickup_zones, on="pickup_location_id", how="left")

# COMMAND ----------

monthly_zone_revenue = (
    trips_enriched
    .withColumn("pickup_month", F.date_trunc("month", F.col("pickup_datetime")))
    .groupBy("pickup_month", "service_type", "pickup_location_id", "pickup_borough", "pickup_zone")
    .agg(
        F.count("*").alias("trips"),
        F.round(F.sum("total_amount"), 2).alias("total_amount"),
        F.round(F.avg("total_amount"), 2).alias("avg_total_amount"),
        F.round(F.sum("trip_distance"), 2).alias("total_trip_distance"),
        F.round(F.avg("trip_duration_minutes"), 2).alias("avg_trip_duration_minutes"),
    )
)

daily_trip_counts = (
    trips_enriched
    .withColumn("pickup_date", F.to_date("pickup_datetime"))
    .groupBy("pickup_date", "service_type")
    .agg(
        F.count("*").alias("trips"),
        F.round(F.sum("total_amount"), 2).alias("total_amount"),
    )
)

# COMMAND ----------

monthly_zone_revenue.write.format("delta").mode("overwrite").option("overwriteSchema", True).saveAsTable(
    f"{gold}.`monthly_zone_revenue`"
)

daily_trip_counts.write.format("delta").mode("overwrite").option("overwriteSchema", True).saveAsTable(
    f"{gold}.`daily_trip_counts`"
)

# COMMAND ----------

display(spark.sql(f"""
SELECT *
FROM {gold}.`monthly_zone_revenue`
ORDER BY total_amount DESC
LIMIT 20
"""))
