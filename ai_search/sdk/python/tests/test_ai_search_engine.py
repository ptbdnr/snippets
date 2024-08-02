import os
import json
from datetime import datetime
from collections.abc import Iterable

import pytest


def test_importable():
    import src.azure_ai_search_engine  # noqa: F401
    from src.azure_ai_search_engine import AzureAISearchEngine  # noqa: F401


@pytest.fixture
def azure_ai_search_config() -> dict:
    return {
        "service_endpoint": os.getenv("SEARCH_ENGINE_AISEARCH_ENDPOINT"),
        "key": os.getenv("SEARCH_ENGINE_AISEARCH_KEY"),
        "index_name": os.getenv("SEARCH_ENGINE_AISEARCH_INDEX_NAME"),
    }


def test_init(azure_ai_search_config):
    from src.azure_ai_search_engine import AzureAISearchEngine
    search_engine = AzureAISearchEngine(**azure_ai_search_config)
    assert search_engine is not None


@pytest.mark.parametrize("text, result_contains_items", [
    ('foo', ['bar']),
    ('buz', ['Joe', 'Doe']),
    ('missing', []),
])
def test_search(azure_ai_search_config, text, result_contains_items):
    from src.azure_ai_search_engine import AzureAISearchEngine
    search_engine = AzureAISearchEngine(**azure_ai_search_config)
    responses = search_engine.search(text=text)
    assert responses is not None
    assert isinstance(responses, Iterable)
    for response in responses:
        assert isinstance(response, dict)
        response_str = json.dumps(response)
        for item in result_contains_items:
            assert item in response_str


@pytest.mark.parametrize("index_name, schema", [
    (
        f"test1-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        {
            'keyField':
                {'field_type': 'simple', 'data_type': 'string', 'key': True}
        }
    ),
    (
        f"test2-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        {
            'keyField':
                {'field_type': 'simple', 'data_type': 'string', 'key': True},
            'vectorField': {
                'field_type': 'search',
                'data_type': 'vector',
                'searchable': True,
                'vector_search_dimensions': 2,
                }
        }
    ),
])
def test_create_index(azure_ai_search_config, index_name, schema):
    from src.azure_ai_search_engine import AzureAISearchEngine
    search_engine = AzureAISearchEngine(**azure_ai_search_config)
    search_index = search_engine.create_index(
        index_name=index_name, 
        schema=schema
    )
    assert search_index is not None
    assert index_name in search_engine.search_index_client.list_index_names()
    search_engine.search_index_client.delete_index(search_index.name)


@pytest.mark.parametrize("index_name, schema, docs", [
    (
        f"test-k-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        {'keyField':
            {'field_type': 'simple', 'data_type': 'string', 'key': True}},
        [{'keyField': '1'}, {'keyField': '2'}],
    ),
    (
        f"test-kv-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        {
            'keyField': 
                {'field_type': 'simple', 'data_type': 'string', 'key': True},
            'vectorField': {
                'field_type': 'search',
                'data_type': 'vector',
                'searchable': True,
                'vector_search_dimensions': 2,
                }
        },
        [
            {"keyField": "1", "vectorField": [0.1, -0.2]},
            {"keyField": "2", "vectorField": [0.3, -0.4]},
        ],
    )
])
def test_upload_documents(azure_ai_search_config, index_name, schema, docs):
    from src.azure_ai_search_engine import AzureAISearchEngine
    search_engine = AzureAISearchEngine(**azure_ai_search_config)
    search_index = search_engine.create_index(
        index_name=index_name,
        schema=schema
    )
    search_engine.upload_documents(index_name=index_name, documents=docs)
    search_engine.search_index_client.delete_index(search_index.name)
