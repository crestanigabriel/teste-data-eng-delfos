from dagster import (
    AssetSelection,
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules,
)

from . import assets
from .resources import SourceDBResource, TargetDBResource

all_assets = load_assets_from_modules([assets])

etl_job = define_asset_job("etl_job", selection=AssetSelection.all())

etl_schedule = ScheduleDefinition(
    job=etl_job,
    cron_schedule="0 5 * * *",  # every day at 5am
)

defs = Definitions(
    assets=all_assets,
    schedules=[etl_schedule],
    resources={
        "source_db": SourceDBResource(),
        "target_db": TargetDBResource(),
    },
)
