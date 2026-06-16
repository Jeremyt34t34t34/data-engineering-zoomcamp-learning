from __future__ import annotations

import argparse
from pathlib import Path

import duckdb
import requests


BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"


def sql_string(value: Path | str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def download_and_convert(taxi_type: str, year: int, month: int) -> None:
    data_dir = Path("data") / taxi_type
    data_dir.mkdir(exist_ok=True, parents=True)

    parquet_path = data_dir / f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
    if parquet_path.exists():
        print(f"Skipping {parquet_path}")
        return

    csv_gz_path = data_dir / f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
    url = f"{BASE_URL}/{taxi_type}/{csv_gz_path.name}"
    print(f"Downloading {url}")

    with requests.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()
        with csv_gz_path.open("wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)

    print(f"Converting {csv_gz_path} -> {parquet_path}")
    con = duckdb.connect()
    con.execute(
        f"""
        COPY (
            SELECT * FROM read_csv_auto({sql_string(csv_gz_path)}, union_by_name=true)
        )
        TO {sql_string(parquet_path)} (FORMAT PARQUET)
        """
    )
    con.close()
    csv_gz_path.unlink()


def refresh_raw_tables() -> None:
    con = duckdb.connect("taxi_rides_ny.duckdb")
    con.execute("CREATE SCHEMA IF NOT EXISTS prod")
    for taxi_type in ["yellow", "green"]:
        con.execute(
            f"""
            CREATE OR REPLACE TABLE prod.{taxi_type}_tripdata AS
            SELECT *
            FROM read_parquet('data/{taxi_type}/*.parquet', union_by_name=true)
            """
        )
    con.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load NYC taxi data into DuckDB.")
    parser.add_argument("--start-year", type=int, default=2019)
    parser.add_argument("--end-year", type=int, default=2020)
    parser.add_argument("--start-month", type=int, default=1)
    parser.add_argument("--end-month", type=int, default=12)
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Only load 2019-01 for yellow and green taxi data.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.sample:
        years = [2019]
        months = [1]
    else:
        years = range(args.start_year, args.end_year + 1)
        months = range(args.start_month, args.end_month + 1)

    for taxi_type in ["yellow", "green"]:
        for year in years:
            for month in months:
                download_and_convert(taxi_type, year, month)

    refresh_raw_tables()
    print("Raw DuckDB tables ready: prod.yellow_tripdata, prod.green_tripdata")


if __name__ == "__main__":
    main()
