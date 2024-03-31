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
import sys

import httpx
import pandas as pd


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
    base_url = "http://localhost:8000"
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

    aggregation = {}
    aggregation_funcs = ["mean", "max", "min", "std"]
    for func in aggregation_funcs:
        aggregation[func] = df.groupby(
            pd.Grouper(key="timestamp", freq="20min", origin="start")
        ).agg(func)
        print(aggregation[func])

    # Store result data on target_db
    """
    Salva o dado no banco de dados Alvo. A escrita no banco de dados deverá utilizar a biblioteca
    sqlalchemy para se conectar ao banco. A escrita do dado no banco pode ser feita com qualquer
    tecnologia, mas recomenda-se o uso do pandas em conjunto com o sqlalchemy.
    """


if __name__ == "__main__":
    main()
