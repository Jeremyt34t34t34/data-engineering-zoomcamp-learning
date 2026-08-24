# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Load Bronze
# MAGIC
# MAGIC Bronze tables keep the source data close to raw form.
# MAGIC
# MAGIC This mirrors the `source()` layer from the Module 4 dbt project.

# COMMAND ----------

dbutils.widgets.text("catalog", "hive_metastore")
dbutils.widgets.text("source_base", "dbfs:/FileStore/de_zoomcamp/taxi")

catalog = dbutils.widgets.get("catalog")
source_base = dbutils.widgets.get("source_base").rstrip("/")

bronze = f"`{catalog}`.`bronze`"

yellow_path = f"{source_base}/yellow/yellow_tripdata_2019-01.parquet"
green_path = f"{source_base}/green/green_tripdata_2019-01.parquet"
zones_path = f"{source_base}/taxi_zone_lookup.csv"

print(f"Reading yellow: {yellow_path}")
print(f"Reading green: {green_path}")
print(f"Reading zones: {zones_path}")

# COMMAND ----------

yellow_raw = spark.read.parquet(yellow_path)
green_raw = spark.read.parquet(green_path)
zones_raw = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(zones_path)
)

# COMMAND ----------

yellow_raw.write.format("delta").mode("overwrite").option("overwriteSchema", True).saveAsTable(
    f"{bronze}.`yellow_taxi_trips_raw`"
)

green_raw.write.format("delta").mode("overwrite").option("overwriteSchema", True).saveAsTable(
    f"{bronze}.`green_taxi_trips_raw`"
)

zones_raw.write.format("delta").mode("overwrite").option("overwriteSchema", True).saveAsTable(
    f"{bronze}.`taxi_zones_raw`"
)

# COMMAND ----------

display(spark.sql(f"""
SELECT 'yellow' AS source, COUNT(*) AS rows FROM {bronze}.`yellow_taxi_trips_raw`
UNION ALL
SELECT 'green' AS source, COUNT(*) AS rows FROM {bronze}.`green_taxi_trips_raw`
UNION ALL
SELECT 'zones' AS source, COUNT(*) AS rows FROM {bronze}.`taxi_zones_raw`
"""))
