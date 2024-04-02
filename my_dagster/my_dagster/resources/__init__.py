from dagster import ConfigurableResource
import httpx


class SourceDBResource(ConfigurableResource):
    def get_data(self, endpoint: str) -> httpx.Response:
        return


class TargetDBResource(ConfigurableResource):
    def post_data(self, endpoint: str) -> httpx.Response:
        return
