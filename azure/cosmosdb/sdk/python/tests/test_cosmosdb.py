import os
import datetime

import pytest


def test_importable():
    import src.cosmosdb  # noqa: F401
    from src.cosmosdb import CosmosDB  # noqa: F401


@pytest.fixture
def now_microsecond() -> str:
    """
    Return current datetime in microsecond format
    @return: str
    """
    return datetime.datetime.now().isoformat(timespec='microseconds')


@pytest.fixture
def azure_cosmosdb_config() -> dict:
    """
    Load environment variables
    @return: dict with Azure CosmosDB configuration
    """
    return {
        'host': os.getenv("DATA_STORE_COSMOSDB_HOST"),
        'key': os.getenv("DATA_STORE_COSMOSDB_KEY"),
        'database_id': os.getenv("DATA_STORE_COSMOSDB_DATABASE_ID"),
        'container_id': os.getenv("DATA_STORE_COSMOSDB_TEST_CONTAINER_ID"),
        'partition_key': os.getenv("DATA_STORE_COSMOSDB_TEST_PARTITION_KEY"),
    }


def test_init(azure_cosmosdb_config):
    from src.cosmosdb import CosmosDB
    data_store = CosmosDB(**azure_cosmosdb_config)
    assert data_store is not None


@pytest.mark.parametrize("item", [
    {'id': 'v1.00', 'key_1': 'bar', 'key_2': 'buz'},
])
def test_insert_item(self, item, azure_cosmosdb_config, now_microsecond):
    item['id'] = item['id'] + '-' + now_microsecond
    from src.cosmosdb import CosmosDB
    data_store = CosmosDB(**azure_cosmosdb_config)
    data_store.insert_item(item)


@pytest.mark.parametrize("max_item_count", [
    1, 10
])
def test_read_items(self, max_item_count, azure_cosmosdb_config):
    from src.cosmosdb import CosmosDB
    data_store = CosmosDB(**azure_cosmosdb_config)
    items = data_store.read_items(max_item_count=max_item_count)
    assert items is not None
    assert isinstance(items, list), f"Expected list, but got {type(items)}"
    assert len(items) <= max_item_count

@pytest.mark.parametrize("field_name_value", [
    {'key_1': 'bar'}
])
def test_query_items(self, field_name_value, azure_cosmosdb_config):
    from src.cosmosdb import CosmosDB
    data_store = CosmosDB(**azure_cosmosdb_config)
    responses = data_store.query_items(field_name_value=field_name_value)
    assert responses is not None
    assert isinstance(responses, list), \
        f"Expected list, but got {type(responses)}"
    for response in responses:
        assert isinstance(response, dict)
