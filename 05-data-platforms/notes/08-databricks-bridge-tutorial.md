# 5.7 - Databricks Bridge Tutorial

## Goal

This is an optional replacement path for the Bruin Cloud part of Module 5.

Use it when you want to learn a more mainstream data platform and prepare for the next modules:

```text
Module 5: Databricks as a data platform
Module 6: Spark batch processing
Module 7: Streaming concepts
```

The goal is not to master all of Databricks. The goal is to understand what Databricks is for, build a small lakehouse mental model, and make the next Spark and streaming chapters feel connected.

## What Databricks replaces in this module

Bruin Cloud is a managed platform for pipelines: ingestion, transformations, orchestration, data quality, lineage, and monitoring.

Databricks is broader and more mainstream. In this replacement path, use Databricks to understand the same platform ideas:

| Data platform idea | Bruin Cloud version | Databricks version |
| --- | --- | --- |
| Store data | Connected warehouse or database | Delta tables in a lakehouse |
| Transform data | SQL/Python assets | Spark, PySpark, SQL, notebooks, pipelines |
| Orchestrate work | Bruin pipeline runs | Databricks Jobs / Workflows |
| Check quality | Bruin checks | SQL checks, expectations, Delta constraints, monitoring patterns |
| Track lineage | Bruin lineage | Unity Catalog lineage |
| Govern access | Cloud connections and permissions | Unity Catalog permissions |
| Query data | Connected warehouse | Databricks SQL warehouse |

In short:

```text
Bruin teaches pipeline platform thinking.
Databricks teaches lakehouse platform thinking.
```

For a data engineering career, Databricks is usually a stronger signal.

## Lesson 1: What problem does Databricks solve?

Companies often start with disconnected tools:

```text
Object storage for raw files
Warehouse for SQL analytics
Spark cluster for big data jobs
Airflow for orchestration
BI tool for dashboards
ML platform for models
Catalog tool for permissions and lineage
```

Databricks tries to bring many of these workflows into one lakehouse platform:

```text
Cloud storage
  -> Delta Lake tables
  -> Spark / SQL / ML workloads
  -> Jobs and workflows
  -> Unity Catalog governance
  -> BI, dashboards, and AI/ML
```

The important idea is that Databricks is not just a database and not just Spark. It is a workspace for building, running, governing, and querying data products.

### Connect to previous modules

- From Module 3: BigQuery taught you cloud warehouse thinking.
- From Module 4: dbt taught you transformation layers and marts.
- From Module 5: Bruin teaches pipeline platform thinking.

Databricks combines parts of all three, but with Spark and Delta Lake as central pieces.

### Connect to next modules

- Module 6 teaches Spark directly. Databricks uses Spark heavily.
- Module 7 teaches streaming concepts. Databricks supports Spark Structured Streaming and incremental ingestion patterns.

## Lesson 2: The lakehouse idea

A data warehouse is great for structured SQL analytics.

A data lake is great for storing large amounts of raw files cheaply.

A lakehouse tries to combine both:

```text
Data lake storage
  + table reliability
  + SQL performance
  + governance
  + support for BI, data engineering, and ML
```

Databricks' version of this usually centers around:

- Cloud object storage: S3, GCS, or ADLS
- Delta Lake: reliable table format on top of files
- Spark: distributed compute engine
- Databricks SQL: SQL analytics experience
- Unity Catalog: governance and lineage

### Why this matters before Spark

In Module 6, Spark can read and write files directly. That is useful, but in real platforms you usually do not want random scripts writing unmanaged parquet folders forever.

Databricks adds a managed lakehouse layer around that work:

```text
Raw parquet files
  -> Delta table
  -> governed table in a catalog
  -> scheduled job
  -> downstream SQL / BI / ML users
```

## Lesson 3: Delta Lake

Delta Lake is one of the most important Databricks concepts.

Plain parquet files are just files. They are fast and common, but they do not automatically give you database-like guarantees.

Delta Lake adds a transaction log around files so tables can support features like:

- ACID transactions
- Schema enforcement
- Schema evolution
- Time travel / table history
- Upserts and deletes
- More reliable batch and streaming pipelines

For now, remember this:

```text
Parquet = file format
Delta Lake = table format built on files plus transaction log
```

### Connect to Module 6

When Module 6 teaches:

```python
df.write.parquet("output/path")
```

Databricks often pushes you toward:

```python
df.write.format("delta").mode("overwrite").saveAsTable("catalog.schema.table")
```

The Spark DataFrame idea is the same. The target table layer is more production-oriented.

## Lesson 4: Bronze, Silver, Gold

Databricks commonly explains lakehouse pipelines with medallion architecture:

```text
Bronze = raw data
Silver = cleaned and validated data
Gold   = business-ready data
```

Map that to what you already learned:

| Zoomcamp / dbt idea | Databricks idea |
| --- | --- |
| Raw source files | Bronze |
| Staging models | Silver-ish |
| Intermediate models | Silver |
| Mart models | Gold |
| Fact and dimension tables | Gold |

This is not a strict one-to-one rule. It is a mental model.

### Tiny NYC taxi design

Use the same taxi dataset from the course:

```text
bronze.yellow_taxi_trips
  Raw trip records loaded from parquet

silver.yellow_taxi_trips_cleaned
  Casted columns, invalid timestamps removed, bad records filtered

silver.taxi_zones
  Cleaned zone lookup table

gold.monthly_zone_revenue
  Monthly revenue by pickup zone

gold.daily_trip_counts
  Daily trips by pickup date
```

### Why this helps later

Module 6 will teach Spark transformations. You can mentally place each transformation into one of these layers:

```text
read raw data -> Bronze
clean/filter/join -> Silver
aggregate/report -> Gold
```

## Lesson 5: Workspace, notebooks, and compute

Databricks work usually happens inside a workspace.

You will see:

- Notebooks: interactive SQL/Python/Scala/R development
- Clusters or compute: machines that run your code
- SQL warehouses: compute for SQL and BI workloads
- Jobs: scheduled or triggered production runs
- Catalog Explorer: browse catalogs, schemas, tables, lineage, and permissions

The key cost idea:

```text
Storage can sit there.
Compute costs money while it runs.
```

When learning, prefer small datasets, short sessions, and shut down compute when done.

## Lesson 6: Databricks Jobs

Jobs are how Databricks turns notebooks or scripts into repeatable workflows.

A simple job can be:

```text
Task 1: load bronze table
Task 2: build silver cleaned table
Task 3: build gold aggregates
```

This is the Databricks version of orchestration.

Compare with earlier tools:

| Tool | Orchestration concept |
| --- | --- |
| Kestra | Flows and tasks |
| Airflow | DAGs and operators |
| Bruin | Pipelines and assets |
| Databricks | Jobs and tasks |

Do not memorize every UI button. Understand the common pattern:

```text
task dependency + schedule + parameters + logs + retries + alerts
```

That pattern repeats across orchestration tools.

## Lesson 7: Unity Catalog

Unity Catalog is Databricks' governance layer.

It helps answer:

- Who can read this table?
- Who can write to this schema?
- Where did this table come from?
- Which downstream reports depend on this data?
- How do we organize data across teams?

Basic hierarchy:

```text
catalog
  schema
    table
    view
    function
```

Example:

```text
de_zoomcamp
  bronze
    yellow_taxi_trips
  silver
    yellow_taxi_trips_cleaned
  gold
    monthly_zone_revenue
```

### Connect to dbt

In dbt, you saw models, schemas, docs, tests, and lineage.

In Databricks, Unity Catalog covers more of the platform governance side: permissions, catalogs, schemas, lineage, and data ownership.

## Lesson 8: How this prepares you for Module 6

Module 6 teaches Spark. Databricks makes Spark feel real-world.

When you see this in Module 6:

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("test").getOrCreate()
df = spark.read.parquet("yellow_tripdata.parquet")
```

Translate it to Databricks thinking:

```text
SparkSession
  -> Databricks gives you Spark through managed compute

DataFrame
  -> same core abstraction

read.parquet
  -> read raw cloud files or Bronze data

write.parquet
  -> in production, often write Delta tables

Spark SQL
  -> Databricks SQL and notebook SQL cells
```

The Spark concepts that matter most for Databricks:

- DataFrames
- Spark SQL
- Partitions
- Joins
- GroupBy and shuffles
- Writing tables
- Reading from object storage

## Lesson 9: How this prepares you for Module 7

Module 7 teaches streaming with Kafka and stream processing tools.

Databricks connects to that world through:

- Spark Structured Streaming
- Streaming reads from files or message systems
- Incremental processing into Delta tables
- Jobs that trigger when new data arrives
- Bronze/Silver/Gold streaming pipelines

You do not need to learn all of this before Module 7.

Just keep this map:

```text
Kafka / event source
  -> streaming ingestion
  -> Bronze Delta table
  -> Silver cleaned stream/table
  -> Gold real-time aggregate
```

That is the streaming version of the same lakehouse pattern.

## A practical study route

Use this as your replacement path for the Bruin Cloud lesson:

1. Read [5.6 - Databricks Primer](07-databricks-primer.md).
2. Read this tutorial through Lesson 7.
3. Watch or read an official Databricks beginner tutorial.
4. Build the tiny NYC taxi design on a small sample, if you have safe/free Databricks access.
5. Continue to Module 6 Spark.
6. After Module 6, revisit this tutorial and connect each Spark concept back to Delta tables and Jobs.
7. After Module 7, revisit Lesson 9 and connect Kafka/streaming to Bronze/Silver/Gold.

## Optional hands-on checklist

Only do this if you have a safe Databricks environment and understand the cost model.

### Step 1: Create a small workspace exercise

Create a notebook called:

```text
nyc_taxi_lakehouse_intro
```

### Step 2: Load a tiny taxi sample

Use a small parquet sample from the NYC taxi data, not the full dataset at first.

Pseudo-code:

```python
df = spark.read.parquet("/path/to/yellow_tripdata_sample.parquet")
display(df.limit(10))
```

### Step 3: Save Bronze

```python
df.write.format("delta").mode("overwrite").saveAsTable("de_zoomcamp.bronze.yellow_taxi_trips")
```

### Step 4: Build Silver

```python
from pyspark.sql import functions as F

silver = (
    df
    .filter(F.col("tpep_pickup_datetime").isNotNull())
    .filter(F.col("tpep_dropoff_datetime").isNotNull())
    .filter(F.col("tpep_dropoff_datetime") > F.col("tpep_pickup_datetime"))
    .filter(F.col("total_amount") >= 0)
)

silver.write.format("delta").mode("overwrite").saveAsTable("de_zoomcamp.silver.yellow_taxi_trips_cleaned")
```

### Step 5: Build Gold

```python
gold = (
    silver
    .withColumn("pickup_month", F.date_trunc("month", F.col("tpep_pickup_datetime")))
    .groupBy("pickup_month", "PULocationID")
    .agg(
        F.count("*").alias("trips"),
        F.sum("total_amount").alias("total_amount")
    )
)

gold.write.format("delta").mode("overwrite").saveAsTable("de_zoomcamp.gold.monthly_zone_revenue")
```

### Step 6: Turn it into a Job

Split the work into three notebooks or tasks:

```text
01_load_bronze
02_build_silver
03_build_gold
```

Then create a Databricks Job:

```text
01_load_bronze -> 02_build_silver -> 03_build_gold
```

This is the Databricks replacement for the Bruin Cloud deployment idea.

## What to remember

If you remember only one map, remember this:

```text
Databricks
  = Lakehouse platform
  = Spark compute + Delta tables + SQL + Jobs + Unity Catalog

Module 6 Spark
  = the compute model underneath many Databricks data engineering workflows

Module 7 Streaming
  = the event/incremental version of the same pipeline thinking
```

## Official references

- [What is Databricks?](https://docs.databricks.com/aws/en/introduction/)
- [What is a data lakehouse?](https://docs.databricks.com/aws/en/lakehouse/)
- [What is the medallion lakehouse architecture?](https://docs.databricks.com/aws/en/lakehouse/medallion)
- [What is Delta Lake in Databricks?](https://docs.databricks.com/aws/en/delta/)
- [What is Unity Catalog?](https://docs.databricks.com/aws/en/data-governance/unity-catalog/)
- [Lakeflow Jobs](https://docs.databricks.com/aws/en/jobs/)
