# Module 4 Homework: Analytics Engineering with dbt

## Submission Form

Course form: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw4

## Answers

### Question 1

Answer: `int_trips_unioned` only

Explanation: `dbt run --select int_trips_unioned` selects only that model. To include upstream dependencies, use `+int_trips_unioned`; to include downstream dependencies, use `int_trips_unioned+`.

### Question 2

Answer: dbt will fail the test, returning a non-zero exit code

Explanation: `accepted_values` is a data test. If `payment_type = 6` appears but the allowed values are only `[1, 2, 3, 4, 5]`, the test returns failing rows and dbt exits with an error.

### Question 3

Answer: 12,184

Query:

```sql
select count(*)
from prod.fct_monthly_zone_revenue;
```

### Question 4

Answer: East Harlem North

Query:

```sql
select
    pickup_zone,
    revenue_monthly_total_amount
from prod.fct_monthly_zone_revenue
where service_type = 'Green'
  and revenue_month >= date '2020-01-01'
  and revenue_month < date '2021-01-01'
order by revenue_monthly_total_amount desc
limit 1;
```

### Question 5

Answer: 384,624

Query:

```sql
select sum(total_monthly_trips)
from prod.fct_monthly_zone_revenue
where service_type = 'Green'
  and revenue_month = date '2019-10-01';
```

### Question 6

Answer: 43,244,693

Query:

```sql
select count(*)
from prod.stg_fhv_tripdata;
```

## Files

- `models/staging/stg_fhv_tripdata.sql`: FHV staging model.
- `models/staging/sources.yml`: adds the `fhv_tripdata` raw source.
- `models/staging/schema.yml`: adds FHV documentation and not-null tests.
- `ingest_taxi_data.py`: supports loading FHV data into DuckDB.

## Local Commands

Run dbt from the course project directory:

```bash
cd 04-analytics-engineering/taxi_rides_ny
HOME="$PWD" dbt debug
HOME="$PWD" dbt build --target prod
```

After loading new raw taxi data, rebuild the incremental fact table from scratch:

```bash
HOME="$PWD" dbt build --target prod --full-refresh
```

## Notes

- Do not commit `target/`, `dbt_packages/`, `.user.yml`, local DuckDB files, credentials, or large datasets.
