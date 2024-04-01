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

import logging

import utils


def main():
    VARS = ["wind_speed", "power"]
    AGG_FUNCS = ["mean", "max", "min", "std"]

    logging.basicConfig(level=logging.DEBUG)

    input_date = utils.parse_input_date()
    df_source = utils.get_data_from_source_db(input_date, fields=VARS)
    df_agg = utils.aggregate_data(df_source, agg_funcs=AGG_FUNCS)
    utils.save_data_on_target_db(df_agg)


if __name__ == "__main__":
    main()
