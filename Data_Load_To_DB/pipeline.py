import click
import pandas as pd
from sqlalchemy import create_engine


@click.command()
@click.option("--db_user", default="postgres", help="Database username")
@click.option("--db_password", default="postgres", help="Database password")
@click.option("--db_host", default="localhost", help="Database host")
@click.option("--db_port", default="5433", help="Database port")
@click.option("--db_name", default="ny_taxi", help="Database name")
@click.option(
    "--trip_path",
    default="Data/green_tripdata_2025-11.parquet",
    help="Path to trip parquet file",
)
@click.option(
    "--zone_path",
    default="Data/taxi_zone_lookup.csv",
    help="Path to zone lookup CSV file",
)
@click.option("--trip_table", default="yellow_taxi_data", help="Trip table name")
@click.option("--zone_table", default="yellow_taxi_zone", help="Zone table name")
def load_data(
    db_user,
    db_password,
    db_host,
    db_port,
    db_name,
    trip_path,
    zone_path,
    trip_table,
    zone_table,
):
    """Load NYC taxi trip and zone data into PostgreSQL."""

    # Build database connection string
    connection_string = (
        f"postgresql://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )
    engine = create_engine(connection_string)

    # Read trip parquet file
    trip_df = pd.read_parquet(trip_path, dtype_backend="pyarrow")

    # Convert float ID columns to nullable integers
    trip_df["RatecodeID"] = trip_df["RatecodeID"].astype("Int16")
    trip_df["passenger_count"] = trip_df["passenger_count"].astype("Int16")
    trip_df["payment_type"] = trip_df["payment_type"].astype("Int16")
    trip_df["trip_type"] = trip_df["trip_type"].astype("Int16")

    # Read taxi zone lookup file
    zone_df = pd.read_csv(zone_path)

    # Write trip data to Postgres
    trip_df.to_sql(trip_table, engine, if_exists="replace", index=False)

    # Write zone data to Postgres
    zone_df.to_sql(zone_table, engine, if_exists="replace", index=False)

    click.echo("Data load completed successfully.")


if __name__ == "__main__":
    load_data()