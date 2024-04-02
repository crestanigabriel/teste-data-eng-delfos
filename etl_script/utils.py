import argparse
import logging
import os

from dotenv import load_dotenv, find_dotenv
import httpx
import pandas as pd

from db import crud, models, schemas
from db.database import engine


def parse_input_date() -> str:
    """
    Recebe uma recebe uma data como input.
    """
    logging.info("Parse input data: beginning...")

    parser = argparse.ArgumentParser(
        description="ETL process - Data Engineer Test at Delfos.",
    )
    parser.add_argument(
        "-d",
        "--date",
        required=True,
        type=str,
        help="date to process ETL (yyyy-mm-dd)",
    )

    args = parser.parse_args()
    input_date = args.date
    logging.info(f"Input data: {input_date}")

    logging.info("Parse input data: done!")
    return input_date


def get_data_from_source_db(input_date: str, fields: list[str]) -> pd.DataFrame | None:
    """
    Consulta dados para variáveis wind_speed e power via API para o dia daquela data. O script deverá se
    consultar a API utilizando a biblioteca httpx.
    """
    logging.info("Get data from source_db: beginning...")

    load_dotenv(find_dotenv("../.env"))
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
        logging.debug(res_json)
        df = pd.DataFrame(res_json)

        if df.empty:
            raise SystemExit(
                "Exiting program: Empty data source. Check the date provided."
            )

        logging.info("Get data from source_db: done!")
        return df
    except httpx.HTTPError as exc:
        logging.error(f"HTTP Exception for {exc.request.url} - {exc}")
        raise SystemExit("Exiting program: Source data fetch error.")


def aggregate_data(df_source: pd.DataFrame, agg_funcs: list[str]) -> pd.DataFrame:
    """
    Agrega o dado 10-minutal com agregações de média, mínimo, máximo e desvio padrão. A
    transformação de dados pode ser implementada com qualquer biblioteca, desde que ela seja
    executada de forma eficiente. Recomenda-se a utilização do pandas ou similar.
    """
    logging.info("Aggregate data: beginning...")

    logging.debug(df_source.head())
    logging.debug(df_source.timestamp.dtype)
    df_source["timestamp"] = pd.to_datetime(df_source["timestamp"])
    logging.debug(df_source.head())
    logging.debug(df_source.timestamp.dtype)

    df_agg = pd.DataFrame()
    for func in agg_funcs:
        df_agg_temp = (
            df_source.groupby(pd.Grouper(key="timestamp", freq="10min", origin="start"))
            .agg(func)
            .reset_index()
        )
        df_agg_temp["func"] = func
        with pd.option_context("display.max_rows", None, "display.max_columns", None):
            logging.debug(df_agg_temp)

        df_agg = pd.concat([df_agg, df_agg_temp], ignore_index=True)

    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        logging.debug(df_agg)

    logging.info("Aggregate data: done!")
    return df_agg


def save_data_on_target_db(df_agg: pd.DataFrame):
    """
    Salva o dado no banco de dados Alvo. A escrita no banco de dados deverá utilizar a biblioteca
    sqlalchemy para se conectar ao banco. A escrita do dado no banco pode ser feita com qualquer
    tecnologia, mas recomenda-se o uso do pandas em conjunto com o sqlalchemy.
    """
    logging.info("Save data on target_db: beginning...")

    models.Base.metadata.create_all(bind=engine)

    df_signals = pd.read_sql_table("signal", con=engine)
    logging.debug(df_signals)

    df_melted = pd.melt(
        df_agg,
        id_vars=["timestamp", "func"],
        value_vars=["wind_speed", "power"],
        var_name="name",
    )
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        logging.debug(df_melted)
        df_melted_merged = df_melted.merge(
            df_signals,
            how="left",
            on=["name", "func"],
        )
        df_melted_merged.rename(columns={"id": "signal_id"}, inplace=True)
        logging.debug(df_melted_merged)

        df_melted_merged.drop(["name", "func"], axis=1, inplace=True)
        logging.debug(df_melted_merged)

        # Sort data
        df_melted_merged.sort_values(by=["timestamp", "signal_id"], inplace=True)

    try:
        rows_affected = df_melted_merged.to_sql(
            "data", con=engine, if_exists="append", index=False
        )
        logging.debug(f"Rows affected: {rows_affected}")
        logging.info("Save data on target_db: done!")
    except Exception as exc:
        logging.error(exc)
