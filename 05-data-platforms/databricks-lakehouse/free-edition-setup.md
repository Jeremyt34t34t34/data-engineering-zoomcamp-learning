# Databricks Free Edition Setup

Use Databricks Free Edition for this mini project before considering any paid workspace.

Official entry point:

- https://www.databricks.com/learn/free-edition

## Goal

Run the Zoomcamp NYC Taxi lakehouse pipeline in a low-risk learning environment:

```text
local course files
  -> upload to Databricks Free Edition
  -> Bronze Delta tables
  -> Silver cleaned trips
  -> Gold analytics tables
  -> quality checks
```

## Step 1: Create or open Free Edition

1. Go to https://www.databricks.com/learn/free-edition
2. Sign up or log in.
3. Open the Databricks workspace.

Avoid creating a normal cloud workspace unless you intentionally want to use a paid trial or paid cloud resources.

## Step 2: Upload course data

Upload these local files:

```text
04-analytics-engineering/taxi_rides_ny/data/yellow/yellow_tripdata_2019-01.parquet
04-analytics-engineering/taxi_rides_ny/data/green/green_tripdata_2019-01.parquet
04-analytics-engineering/taxi_rides_ny/seeds/taxi_zone_lookup.csv
```

Target paths expected by the notebooks:

```text
dbfs:/FileStore/de_zoomcamp/taxi/yellow/yellow_tripdata_2019-01.parquet
dbfs:/FileStore/de_zoomcamp/taxi/green/green_tripdata_2019-01.parquet
dbfs:/FileStore/de_zoomcamp/taxi/taxi_zone_lookup.csv
```

If Free Edition gives you a different upload path, keep that path and set the notebook widget `source_base` accordingly.

For example, if files are under:

```text
dbfs:/FileStore/shared_uploads/your_email/de_zoomcamp/taxi
```

then use:

```text
source_base = dbfs:/FileStore/shared_uploads/your_email/de_zoomcamp/taxi
```

## Step 3: Import notebooks

Import the notebook source files from:

```text
05-data-platforms/databricks-lakehouse/notebooks/
```

Run them in this order:

```text
00_setup.py
01_load_bronze.py
02_build_silver.py
03_build_gold.py
04_quality_checks.py
```

## Step 4: Use safe defaults

Default widget values:

```text
catalog = hive_metastore
source_base = dbfs:/FileStore/de_zoomcamp/taxi
```

If your Free Edition workspace uses Unity Catalog by default, you may need to replace `hive_metastore` with the available catalog name.

## Step 5: Confirm the tables

After the notebooks run, you should see:

```text
bronze.yellow_taxi_trips_raw
bronze.green_taxi_trips_raw
bronze.taxi_zones_raw

silver.yellow_taxi_trips_cleaned
silver.green_taxi_trips_cleaned
silver.taxi_trips
silver.taxi_zones

gold.monthly_zone_revenue
gold.daily_trip_counts
```

## If upload is blocked

If Free Edition does not allow direct upload of the larger yellow parquet file, use the smaller green parquet first:

```text
04-analytics-engineering/taxi_rides_ny/data/green/green_tripdata_2019-01.parquet
```

Then adjust the tutorial to run only the green taxi branch. The platform concepts are the same:

```text
raw file -> Bronze Delta table -> Silver cleaned table -> Gold aggregate
```
