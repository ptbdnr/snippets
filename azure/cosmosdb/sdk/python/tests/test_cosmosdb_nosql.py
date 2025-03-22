import datetime
import os
from dataclasses import asdict

import pytest


def test_importable():
    import src.cosmosdb_nosql  # noqa: F401
    from src.cosmosdb_nosql import CosmosDBNoSQL, CosmosDBNoSQLConfig  # noqa: F401


@pytest.fixture
def now_microsecond() -> str:
    """Return current datetime in microsecond format."""
    return datetime.datetime.now().isoformat(timespec="microseconds")


class TestCosmosDBNoSQL:

    from src.cosmosdb_nosql import CosmosDBNoSQL, CosmosDBNoSQLConfig

    @pytest.fixture
    def azure_cosmosdb_config() -> CosmosDBNoSQLConfig:
        """Load environment variables."""
        from src.cosmosdb_nosql import CosmosDBNoSQLConfig
        return CosmosDBNoSQLConfig(
            host=os.getenv("DATA_STORE_COSMOSDB_HOST", ""),
            key=os.getenv("DATA_STORE_COSMOSDB_KEY", ""),
            database_id=os.getenv("DATA_STORE_COSMOSDB_DATABASE_ID", ""),
            container_id=os.getenv("DATA_STORE_COSMOSDB_TEST_CONTAINER_ID", ""),
            partition_key=os.getenv("DATA_STORE_COSMOSDB_TEST_PARTITION_KEY", ""),
        )


    def test_init(azure_cosmosdb_config):
        from src.cosmosdb_nosql import CosmosDBNoSQL
        data_store = CosmosDBNoSQL(**asdict(azure_cosmosdb_config))
        assert data_store is not None


    @pytest.mark.parametrize("item", [
        {"id": "v1.00", "key_1": "bar", "key_2": "buz"},
    ])
    def test_insert(self, item, azure_cosmosdb_config, now_microsecond):
        item["id"] = item["id"] + "-" + now_microsecond
        from src.cosmosdb_nosql import CosmosDBNoSQL
        data_store = CosmosDBNoSQL(**asdict(azure_cosmosdb_config))
        data_store.insert(item)

    @pytest.mark.parametrize("max_item_count", [1])
    def read_all_items(self, max_item_count, azure_cosmosdb_config):
        from src.cosmosdb_nosql import CosmosDBNoSQL
        data_store = CosmosDBNoSQL(**asdict(azure_cosmosdb_config))
        items = data_store.read_all_items(max_item_count=max_item_count)
        assert items is not None
        assert isinstance(items, list), f"Expected list, but got {type(items)}"
        assert len(items) <= max_item_count

    @pytest.mark.parametrize("field_name_value", [
        {"key_1": "bar"},
    ])
    def test_query_items(self, field_name_value, azure_cosmosdb_config):
        from src.cosmosdb_nosql import CosmosDBNoSQL
        data_store = CosmosDBNoSQL(**asdict(azure_cosmosdb_config))
        responses = data_store.query_items(field_name_value=field_name_value)
        assert responses is not None
        assert isinstance(responses, list), \
            f"Expected list, but got {type(responses)}"
        for response in responses:
            assert isinstance(response, dict)
