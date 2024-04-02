from dagster import (
    asset,
    AssetExecutionContext,
    DailyPartitionsDefinition,
    MaterializeResult,
)
import pandas as pd

from . import utils
from .resources import SourceDBResource, TargetDBResource


@asset
def hello_world() -> MaterializeResult:
    return MaterializeResult(metadata={"message": "Hello world"})


# @asset(partitions_def=DailyPartitionsDefinition(start_date="2024-01-31"))
@asset()
def my_daily_partitioned_asset(
    context: AssetExecutionContext,
    source_db: SourceDBResource,
    target_db: TargetDBResource,
) -> None:
    # partition_date_str = context.partition_key
    # url = f"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={partition_date_str}"
    # target_location = f"nasa/{partition_date_str}.csv"

    VARS = ["wind_speed", "power"]
    AGG_FUNCS = ["mean", "max", "min", "std"]

    # Extract
    df_source = source_db.get_data(input_date="2024-01-31", fields=VARS)
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(df_source)

    # Transform
    df_agg = utils.aggregate_data(df_source, agg_funcs=AGG_FUNCS)

    # Load
    target_db.post_data(df_agg)
