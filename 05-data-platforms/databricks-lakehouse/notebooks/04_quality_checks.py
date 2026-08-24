# Databricks notebook source
# MAGIC %md
# MAGIC # 04 - Quality Checks
# MAGIC
# MAGIC This notebook is the Databricks version of simple dbt tests.
# MAGIC
# MAGIC If any check fails, the notebook raises an error and the Databricks Job fails.

# COMMAND ----------

dbutils.widgets.text("catalog", "hive_metastore")

catalog = dbutils.widgets.get("catalog")
silver = f"`{catalog}`.`silver`"
gold = f"`{catalog}`.`gold`"

# COMMAND ----------

checks = [
    (
        "silver taxi_trips has rows",
        f"SELECT COUNT(*) AS failures FROM {silver}.`taxi_trips` HAVING COUNT(*) = 0",
    ),
    (
        "trip_id is unique",
        f"""
        SELECT COUNT(*) AS failures
        FROM (
            SELECT trip_id, COUNT(*) AS n
            FROM {silver}.`taxi_trips`
            GROUP BY trip_id
            HAVING COUNT(*) > 1
        )
        """,
    ),
    (
        "pickup_datetime is not null",
        f"SELECT COUNT(*) AS failures FROM {silver}.`taxi_trips` WHERE pickup_datetime IS NULL",
    ),
    (
        "dropoff is after pickup",
        f"SELECT COUNT(*) AS failures FROM {silver}.`taxi_trips` WHERE dropoff_datetime <= pickup_datetime",
    ),
    (
        "total_amount is non-negative",
        f"SELECT COUNT(*) AS failures FROM {silver}.`taxi_trips` WHERE total_amount < 0",
    ),
    (
        "gold monthly_zone_revenue has rows",
        f"SELECT COUNT(*) AS failures FROM {gold}.`monthly_zone_revenue` HAVING COUNT(*) = 0",
    ),
]

failed = []

for name, query in checks:
    rows = spark.sql(query).collect()
    failures = rows[0]["failures"] if rows else 0
    print(f"{name}: {failures} failures")
    if failures:
        failed.append((name, failures))

if failed:
    raise Exception(f"Quality checks failed: {failed}")

print("All quality checks passed.")

# COMMAND ----------

display(spark.sql(f"""
SELECT service_type, COUNT(*) AS trips, MIN(pickup_datetime) AS min_pickup, MAX(pickup_datetime) AS max_pickup
FROM {silver}.`taxi_trips`
GROUP BY service_type
ORDER BY service_type
"""))
