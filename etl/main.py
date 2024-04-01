"""
Recebe uma recebe uma data como input,
Consulta dados para variáveis wind_speed e power via API para o dia daquela data. O script deverá se
consultar a API utilizando a biblioteca httpx.
Agrega o dado 10-minutal com agregações de média, mínimo, máximo e desvio padrão. A
transformação de dados pode ser implementada com qualquer biblioteca, desde que ela seja
executada de forma eficiente. Recomenda-se a utilização do pandas ou similar.
Salva o dado no banco de dados Alvo. A escrita no banco de dados deverá utilizar a biblioteca
sqlalchemy para se conectar ao banco. A escrita do dado no banco pode ser feita com qualquer
tecnologia, mas recomenda-se o uso do pandas em conjunto com o sqlalchemy.
"""

import argparse
from datetime import date, datetime
import os
import sys

from dotenv import load_dotenv, find_dotenv
import httpx
import pandas as pd

from db import crud, models, schemas
from db.database import SessionLocal, engine


def main():
    ## Parsing input date
    """
    Recebe uma recebe uma data como input.
    """

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
    print(f"Input data: {input_date}")

    ## Get (wind_speed, power) variables from source_db_api at input_date
    """
    Consulta dados para variáveis wind_speed e power via API para o dia daquela data. O script deverá se
    consultar a API utilizando a biblioteca httpx.
    """
    load_dotenv(find_dotenv("../.env"))
    SOURCE_DB_API_HOST_PORT = os.getenv("SOURCE_DB_API_HOST_PORT")

    base_url = f"http://localhost:{SOURCE_DB_API_HOST_PORT}"
    body = {
        "start_datetime": f"{args.date}T07:00:00",
        "end_datetime": f"{args.date}T08:59:59",
        "fields": ["wind_speed", "power"],
    }
    try:
        res = httpx.post(f"{base_url}/data", json=body)

        if not res.is_error:
            res_json = res.json()
            print(res_json)

            df = pd.DataFrame(res_json)
        else:
            print("Request problem:")
            print(res)
            print(res.json())
    except:
        print("Data fetch failed.")

    ## Aggregate data
    """
    Agrega o dado 10-minutal com agregações de média, mínimo, máximo e desvio padrão. A
    transformação de dados pode ser implementada com qualquer biblioteca, desde que ela seja
    executada de forma eficiente. Recomenda-se a utilização do pandas ou similar.
    """
    print(df.head())
    print(df.timestamp.dtype)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    print(df.head())
    print(df.timestamp.dtype)

    # aggregation = {}
    # aggregation_funcs = ["mean", "max", "min", "std"]
    # for func in aggregation_funcs:
    #     aggregation[func] = df.groupby(
    #         pd.Grouper(key="timestamp", freq="20min", origin="start")
    #     ).agg(func)
    #     aggregation[func] = aggregation[func].reset_index()
    #     print(aggregation[func])
    df_agg = pd.DataFrame()
    agg_funcs = ["mean", "max", "min", "std"]
    for func in agg_funcs:
        df_agg_temp = (
            df.groupby(pd.Grouper(key="timestamp", freq="20min", origin="start"))
            .agg(func)
            .reset_index()
        )
        df_agg_temp["func"] = func
        with pd.option_context("display.max_rows", None, "display.max_columns", None):
            print(df_agg_temp)

        df_agg = pd.concat([df_agg, df_agg_temp], ignore_index=True)

    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(df_agg)

    # Store result data on target_db
    """
    Salva o dado no banco de dados Alvo. A escrita no banco de dados deverá utilizar a biblioteca
    sqlalchemy para se conectar ao banco. A escrita do dado no banco pode ser feita com qualquer
    tecnologia, mas recomenda-se o uso do pandas em conjunto com o sqlalchemy.
    """
    models.Base.metadata.create_all(bind=engine)

    # # Dependency
    # def get_db():
    #     db = SessionLocal()
    #     try:
    #         yield db
    #     finally:
    #         db.close()
    # db = SessionLocal()

    # signals = crud.get_signal(db)
    # print(type(signals))
    # for signal in signals:
    #     import json

    #     print(vars(signal))

    # df_signals = pd.DataFrame.from_records([s.to_dict() for s in signals])
    # print(df_signals.head())

    df_signals = pd.read_sql_table("signal", con=engine)
    # df_signals.set_index("id", inplace=True)
    print(df_signals)

    # df_melted = pd.melt(
    #     aggregation["mean"],
    #     id_vars=["timestamp"],
    #     value_vars=["wind_speed", "power"],
    #     var_name="name",
    # )
    # with pd.option_context(
    #     "display.max_rows", None, "display.max_columns", None
    # ):  # more options can be specified also
    #     print(aggregation["mean"])
    #     df_melted["func"] = "mean"
    #     print(df_melted)
    #     df_melted_merged = df_melted.merge(
    #         df_signals,
    #         how="left",
    #         on=["name", "func"],
    #         suffixes=("_left", "_right"),
    #     )
    #     print(df_melted_merged)
    df_melted = pd.melt(
        df_agg,
        id_vars=["timestamp", "func"],
        value_vars=["wind_speed", "power"],
        var_name="name",
    )
    with pd.option_context(
        "display.max_rows", None, "display.max_columns", None
    ):  # more options can be specified also
        print(df_melted)
        df_melted_merged = df_melted.merge(
            df_signals,
            how="left",
            on=["name", "func"],
        )
        df_melted_merged.rename(columns={"id": "signal_id"}, inplace=True)
        print(df_melted_merged)

        df_melted_merged.drop(["name", "func"], axis=1, inplace=True)
        print(df_melted_merged)

    rows_affected = df_melted_merged.to_sql(
        "data", con=engine, if_exists="append", index=False
    )
    print(f"Rows affected: {rows_affected}")

    # db.close()


if __name__ == "__main__":
    main()
