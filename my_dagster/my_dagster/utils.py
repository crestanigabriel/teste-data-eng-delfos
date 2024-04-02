import pandas as pd


def aggregate_data(df_source: pd.DataFrame, agg_funcs: list[str]) -> pd.DataFrame:
    """
    Agrega o dado 10-minutal com agregações de média, mínimo, máximo e desvio padrão. A
    transformação de dados pode ser implementada com qualquer biblioteca, desde que ela seja
    executada de forma eficiente. Recomenda-se a utilização do pandas ou similar.
    """
    # logging.debug(df_source.head())
    # logging.debug(df_source.timestamp.dtype)
    df_source["timestamp"] = pd.to_datetime(df_source["timestamp"])
    # logging.debug(df_source.head())
    # logging.debug(df_source.timestamp.dtype)

    df_agg = pd.DataFrame()
    for func in agg_funcs:
        df_agg_temp = (
            df_source.groupby(pd.Grouper(key="timestamp", freq="10min", origin="start"))
            .agg(func)
            .reset_index()
        )
        df_agg_temp["func"] = func
        # with pd.option_context("display.max_rows", None, "display.max_columns", None):
        #     logging.debug(df_agg_temp)

        df_agg = pd.concat([df_agg, df_agg_temp], ignore_index=True)

    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        # logging.debug(df_agg)
        print(df_agg)

    return df_agg
