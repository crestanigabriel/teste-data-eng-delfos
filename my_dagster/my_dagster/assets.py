from dagster import (
    asset,
    AssetExecutionContext,
    DailyPartitionsDefinition,
    MaterializeResult,
)
import pandas as pd

from . import utils
from .resources import SourceDBResource, TargetDBResource


@asset(
    partitions_def=DailyPartitionsDefinition(
        start_date="2024-01-01", end_date="2024-01-12"
    )
)
def my_daily_partitioned_asset(
    context: AssetExecutionContext,
    source_db: SourceDBResource,
    target_db: TargetDBResource,
) -> None:
    partition_date_str = context.partition_key

    VARS = ["wind_speed", "power"]
    AGG_FUNCS = ["mean", "max", "min", "std"]

    # Extract
    df_source = source_db.get_data(input_date=partition_date_str, fields=VARS)
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(df_source)

    # Transform
    df_agg = utils.aggregate_data(df_source, agg_funcs=AGG_FUNCS)

    # Load
    target_db.post_data(df_agg)
