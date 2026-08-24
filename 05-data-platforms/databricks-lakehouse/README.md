# Databricks Lakehouse Mini Project

This optional project replaces the Bruin Cloud hands-on path with a mainstream Databricks lakehouse exercise.

It reuses the Zoomcamp NYC Taxi data from Module 4:

```text
04-analytics-engineering/taxi_rides_ny/data/yellow/yellow_tripdata_2019-01.parquet
04-analytics-engineering/taxi_rides_ny/data/green/green_tripdata_2019-01.parquet
04-analytics-engineering/taxi_rides_ny/seeds/taxi_zone_lookup.csv
```

The pipeline mirrors the dbt project you already studied:

```text
Raw parquet/csv files
  -> Bronze raw Delta tables
  -> Silver cleaned and unioned trips
  -> Gold analytics tables
  -> Quality checks
```

## What this teaches

- How course parquet files become Delta tables
- How Bronze/Silver/Gold maps to dbt raw/staging/marts
- How Databricks notebooks use Spark DataFrames
- How a Databricks Job can replace a Bruin Cloud pipeline run
- How this prepares you for Module 6 Spark

## Files

```text
databricks-lakehouse/
  README.md
  databricks.yml
  notebooks/
    00_setup.py
    01_load_bronze.py
    02_build_silver.py
    03_build_gold.py
    04_quality_checks.py
```

## Data upload

Use Databricks Free Edition first:

- [Free Edition setup](free-edition-setup.md)

Before running the notebooks, upload these local files to Databricks:

```text
Local:
  04-analytics-engineering/taxi_rides_ny/data/yellow/yellow_tripdata_2019-01.parquet
  04-analytics-engineering/taxi_rides_ny/data/green/green_tripdata_2019-01.parquet
  04-analytics-engineering/taxi_rides_ny/seeds/taxi_zone_lookup.csv

Databricks target:
  dbfs:/FileStore/de_zoomcamp/taxi/yellow/yellow_tripdata_2019-01.parquet
  dbfs:/FileStore/de_zoomcamp/taxi/green/green_tripdata_2019-01.parquet
  dbfs:/FileStore/de_zoomcamp/taxi/taxi_zone_lookup.csv
```

You can upload through the Databricks UI, Databricks CLI, or a workspace file upload workflow.

Keep the first run small. January 2019 yellow taxi data is already enough to see the platform pattern.

## Notebook order

Run the notebooks in this order:

```text
00_setup
01_load_bronze
02_build_silver
03_build_gold
04_quality_checks
```

The default table layout is:

```text
hive_metastore.bronze.yellow_taxi_trips_raw
hive_metastore.bronze.green_taxi_trips_raw
hive_metastore.bronze.taxi_zones_raw

hive_metastore.silver.yellow_taxi_trips_cleaned
hive_metastore.silver.green_taxi_trips_cleaned
hive_metastore.silver.taxi_trips
hive_metastore.silver.taxi_zones

hive_metastore.gold.monthly_zone_revenue
hive_metastore.gold.daily_trip_counts
```

If you have Unity Catalog enabled, change the `catalog` widget from `hive_metastore` to your catalog name.

## How this maps to previous modules

| Earlier course concept | Databricks version |
| --- | --- |
| GCS / local parquet files | raw files in DBFS or cloud storage |
| dbt source tables | Bronze Delta tables |
| dbt staging models | Silver cleaned tables |
| dbt marts | Gold tables |
| dbt tests | quality check notebook / table expectations |
| Kestra / Airflow / Bruin pipeline | Databricks Job with ordered tasks |

## How this prepares Module 6

Module 6 teaches Spark. These notebooks use the same core Spark ideas:

```python
df = spark.read.parquet(...)
df = df.filter(...).select(...)
df.groupBy(...).agg(...)
df.write.format("delta").saveAsTable(...)
```

The difference is that Databricks wraps Spark in a lakehouse platform:

```text
Spark DataFrame
  -> Delta table
  -> catalog/schema/table
  -> scheduled Databricks Job
```

## Optional Databricks Asset Bundle

The `databricks.yml` file defines a simple job with five tasks. Use it only after you have configured the Databricks CLI and authenticated to a workspace.

For learning, running the notebooks manually first is better.
