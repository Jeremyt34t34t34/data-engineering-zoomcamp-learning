# 5.6 - Databricks Primer

## Why add Databricks here?

Bruin is useful for understanding the idea of an end-to-end data platform, but it is not as widely used in data engineering job descriptions as Databricks, Snowflake, BigQuery, dbt, Airflow, Spark, or Kafka.

This note is a practical bridge: use Bruin to understand pipeline concepts, then use this Databricks primer to understand a more mainstream lakehouse platform.

## What is Databricks?

Databricks is a cloud data and AI platform built around the lakehouse architecture. It combines ideas from:

- Data lakes: cheap, scalable storage for files and raw data
- Data warehouses: SQL analytics, BI, tables, governance, and performance
- Spark platforms: distributed processing for large batch and streaming workloads
- ML/AI platforms: model training, experiment tracking, serving, and generative AI workflows

In the language of this course:

```text
GCS / S3 / ADLS
  = cloud object storage

BigQuery / Snowflake
  = warehouse-style analytics platforms

Spark / PySpark
  = distributed compute engine

dbt
  = SQL transformation and analytics engineering layer

Databricks
  = managed lakehouse platform combining storage access, Spark compute,
    SQL analytics, jobs, governance, notebooks, Delta tables, and ML/AI tools
```

## Where Databricks fits in the Zoomcamp mental model

The Zoomcamp already teaches many pieces that map directly to Databricks:

| Zoomcamp topic | Databricks equivalent |
| --- | --- |
| Docker / Terraform | Infrastructure and deployment concepts |
| Kestra / orchestration | Databricks Jobs / Workflows |
| GCS data lake | Cloud object storage behind the lakehouse |
| BigQuery warehouse | Databricks SQL / SQL warehouses |
| dbt models | dbt on Databricks or Databricks SQL transformations |
| Spark / PySpark | Databricks Runtime, notebooks, jobs, clusters |
| Kafka streaming | Spark Structured Streaming on Databricks |

The most important overlap is Module 6: Batch Processing with Spark. If Spark DataFrames, Spark SQL, partitions, joins, and cluster execution make sense, Databricks becomes much less mysterious.

## The core Databricks concepts

### Workspace

The browser UI where teams work with notebooks, jobs, dashboards, SQL queries, data catalogs, and settings.

Think of it as the main control room.

### Compute

Databricks runs workloads on managed compute. Depending on the task, this might appear as:

- All-purpose clusters for interactive notebook development
- Job clusters for scheduled production runs
- SQL warehouses for BI and SQL analytics
- Serverless compute options in supported environments

The important idea: storage and compute are separate. Your data usually lives in cloud object storage or managed tables, while compute is started, scaled, and stopped to process it.

### Delta Lake

Delta Lake is the storage layer commonly used with Databricks tables. It adds database-like reliability features on top of data lake files, including transactions, schema enforcement, and table history.

This is why Databricks is not just "Spark reading random parquet files." Delta tables make lake data behave more like managed warehouse tables.

### Unity Catalog

Unity Catalog is Databricks' governance layer. It manages catalogs, schemas, tables, permissions, lineage, and auditing.

A useful mental model:

```text
Unity Catalog
  catalog
    schema
      table / view / function / model
```

In a real company, Unity Catalog is where access control and data ownership become serious.

### Jobs / Workflows

Databricks Jobs are used to schedule and orchestrate repeatable work:

- Run a notebook every day
- Run a Python script with parameters
- Run multiple tasks as a DAG
- Trigger work when new files arrive
- Send alerts when a run fails

This overlaps conceptually with Kestra, Airflow, and Bruin orchestration.

### Notebooks

Databricks notebooks support SQL, Python, Scala, and R. They are popular for exploration, Spark development, and data science.

For production, notebooks are often run through Jobs, or code is moved into Python packages and deployed with Databricks Asset Bundles.

### Medallion architecture

Databricks commonly teaches the lakehouse using Bronze, Silver, and Gold layers:

```text
Bronze = raw ingested data
Silver = cleaned, validated, deduplicated data
Gold   = business-ready aggregates, facts, dimensions, reports
```

This maps nicely to what you already saw in dbt:

```text
staging      ~= Bronze/Silver boundary
intermediate ~= Silver
marts        ~= Gold
```

It is not exactly the same naming system, but the intent is similar: data becomes more trustworthy and more business-ready as it moves downstream.

## Databricks vs Bruin

| Question | Bruin | Databricks |
| --- | --- | --- |
| Main job | Build, run, and monitor data pipelines | Lakehouse platform for data engineering, SQL, ML, AI, and governance |
| Core compute | Runs SQL/Python against connected systems | Managed Spark, SQL warehouses, serverless/job compute |
| Storage layer | Usually external warehouse/database | Lakehouse tables, usually Delta Lake over cloud storage |
| Orchestration | Built into Bruin pipeline model | Databricks Jobs / Workflows |
| Governance | Metadata and lineage features | Unity Catalog, permissions, lineage, audit |
| Job market signal | Smaller/newer | Much more mainstream |

Short version:

```text
Bruin teaches the shape of an end-to-end data platform.
Databricks is a major industry platform where many of those ideas appear at enterprise scale.
```

## Databricks vs Snowflake vs BigQuery

This is oversimplified, but useful:

| Platform | Strong default identity |
| --- | --- |
| BigQuery | Serverless cloud data warehouse on GCP |
| Snowflake | Cloud data warehouse with strong SQL, sharing, and governance ecosystem |
| Databricks | Lakehouse platform with Spark, Delta Lake, ML/AI, SQL, and governance |

Snowflake and BigQuery often feel more SQL-warehouse-first.

Databricks often feels more lakehouse/Spark/data-engineering/ML-first, though Databricks SQL has made it much stronger for warehouse-style analytics.

## What to learn first

If your goal is job readiness, use this order:

1. Finish this camp's Spark module.
2. Learn the Databricks workspace basics: notebooks, clusters, jobs, SQL warehouses.
3. Build a tiny Bronze/Silver/Gold pipeline with PySpark and Delta tables.
4. Learn Unity Catalog vocabulary: catalog, schema, table, external location, permissions, lineage.
5. Learn Databricks Jobs: tasks, dependencies, schedules, parameters, alerts.
6. Only then look at MLflow, model serving, Vector Search, and advanced AI features.

## Small practice project

Use the NYC taxi dataset from the Zoomcamp and rebuild a tiny version of the pipeline in Databricks:

```text
Bronze
  Read raw parquet taxi data from cloud storage or uploaded files.
  Save it as a Delta table.

Silver
  Cast columns.
  Remove invalid timestamps.
  Deduplicate trips.
  Join taxi zone lookup data.

Gold
  Build monthly revenue by pickup zone.
  Build trips by day and service type.

Job
  Schedule Bronze -> Silver -> Gold as separate tasks.

Governance
  Put tables under a catalog/schema.
  Inspect lineage.
```

This mirrors the Zoomcamp pipeline while teaching Databricks-native concepts.

## Official resources

- [What is Databricks?](https://docs.databricks.com/aws/en/introduction/)
- [What is a data lakehouse?](https://docs.databricks.com/aws/en/lakehouse/)
- [What is the medallion lakehouse architecture?](https://docs.databricks.com/aws/en/lakehouse/medallion)
- [What is Delta Lake in Databricks?](https://docs.databricks.com/aws/en/delta/)
- [What is Unity Catalog?](https://docs.databricks.com/aws/en/data-governance/unity-catalog/)
- [Lakeflow Jobs](https://docs.databricks.com/aws/en/jobs/)
- [Free Databricks training](https://docs.databricks.com/aws/en/getting-started/free-training)

## What not to overlearn yet

Do not start with all of Databricks. It is too wide.

For data engineering, your first target should be:

```text
Workspace -> Spark notebook -> Delta table -> Bronze/Silver/Gold -> Job -> Unity Catalog basics
```

That is enough to understand how Databricks fits into modern data engineering.
