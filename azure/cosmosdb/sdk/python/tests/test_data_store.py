import pytest


def test_importable():
    import src.data_store  # noqa: F401
    from src.data_store import DataStore  # noqa: F401
    from src.data_store import DataStoreProvider  # noqa: F401


class TestDataStore:

    from src.data_store import DataStoreProvider

    def test_structure(self):
        from src.data_store import DataStore
        for method in ['new', 'insert_item', 'read_items', 'query_items']:
            assert hasattr(DataStore, method)
            assert callable(getattr(DataStore, method))

    @pytest.mark.parametrize("provider", [
        DataStoreProvider.MOCKUP,
        DataStoreProvider.COSMOSDB,
    ])
    def test_new(self, provider):
        from src.data_store import DataStore
        search_engine = DataStore.new(provider=provider)
        assert search_engine is not None
