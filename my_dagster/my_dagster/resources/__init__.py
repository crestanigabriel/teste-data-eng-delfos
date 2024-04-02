import os

from dagster import ConfigurableResource
import httpx
import pandas as pd
from sqlalchemy import create_engine


class SourceDBResource(ConfigurableResource):
    def get_data(self, input_date: str, fields: list[str]) -> pd.DataFrame:
        SOURCE_DB_API_HOST_PORT = os.getenv("SOURCE_DB_API_HOST_PORT")
        base_url = f"http://localhost:{SOURCE_DB_API_HOST_PORT}"
        body = {
            "start_datetime": f"{input_date}T00:00:00",
            "end_datetime": f"{input_date}T23:59:59",
            "fields": fields,
        }
        try:
            res = httpx.post(f"{base_url}/data", json=body)
            res.raise_for_status()

            res_json = res.json()
            # logging.debug(res_json)
            df = pd.DataFrame(res_json)

            if df.empty:
                raise SystemExit("Exiting program: Empty data source.")

            return df
        except httpx.HTTPError as exc:
            # logging.error(f"HTTP Exception for {exc.request.url} - {exc}")
            raise SystemExit("Exiting program: Source data fetch error.")


class TargetDBResource(ConfigurableResource):
    def post_data(self, df_agg: pd.DataFrame) -> None:
        # Database connection
        DB_USER = os.getenv("POSTGRES_USER")
        DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        DB_DATABASE_NAME = os.getenv("POSTGRES_DB")

        DB_HOST_PORT = os.getenv("TARGET_DB_HOST_PORT")
        DB_HOST_NAME = "localhost"

        # Database connection string
        SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST_NAME}:{DB_HOST_PORT}/{DB_DATABASE_NAME}"
        # logging.debug(f"SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}")

        engine = create_engine(SQLALCHEMY_DATABASE_URL)

        # Saving data
        df_signals = pd.read_sql_table("signal", con=engine)
        # logging.debug(df_signals)

        df_melted = pd.melt(
            df_agg,
            id_vars=["timestamp", "func"],
            value_vars=["wind_speed", "power"],
            var_name="name",
        )
        with pd.option_context("display.max_rows", None, "display.max_columns", None):
            # logging.debug(df_melted)
            df_melted_merged = df_melted.merge(
                df_signals,
                how="left",
                on=["name", "func"],
            )
            df_melted_merged.rename(columns={"id": "signal_id"}, inplace=True)
            # logging.debug(df_melted_merged)

            df_melted_merged.drop(["name", "func"], axis=1, inplace=True)
            # logging.debug(df_melted_merged)

            # Sort data
            df_melted_merged.sort_values(by=["timestamp", "signal_id"], inplace=True)

        rows_affected = df_melted_merged.to_sql(
            "data", con=engine, if_exists="append", index=False
        )
        print(f"Rows affected: {rows_affected}")
        # logging.debug(f"Rows affected: {rows_affected}")
