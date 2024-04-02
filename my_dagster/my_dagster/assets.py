from dagster import (
    asset,
    AssetExecutionContext,
    DailyPartitionsDefinition,
    MaterializeResult,
)


@asset
def hello_world() -> MaterializeResult:
    return MaterializeResult(metadata={"message": "Hello world"})


@asset(partitions_def=DailyPartitionsDefinition(start_date="2024-01-31"))
def my_daily_partitioned_asset(context: AssetExecutionContext) -> None:
    partition_date_str = context.partition_key

    url = f"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date={partition_date_str}"
    target_location = f"nasa/{partition_date_str}.csv"
