# Databricks notebook source
# MAGIC %md
# MAGIC # 00 - Setup
# MAGIC
# MAGIC Creates the schemas used by the mini lakehouse project.
# MAGIC
# MAGIC Default layout:
# MAGIC
# MAGIC ```text
# MAGIC hive_metastore.bronze
# MAGIC hive_metastore.silver
# MAGIC hive_metastore.gold
# MAGIC ```

# COMMAND ----------

dbutils.widgets.text("catalog", "hive_metastore")
dbutils.widgets.text("source_base", "dbfs:/FileStore/de_zoomcamp/taxi")

catalog = dbutils.widgets.get("catalog")
source_base = dbutils.widgets.get("source_base").rstrip("/")

for schema in ["bronze", "silver", "gold"]:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{catalog}`.`{schema}`")

print(f"Catalog: {catalog}")
print(f"Source base: {source_base}")
print("Created schemas: bronze, silver, gold")

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS
