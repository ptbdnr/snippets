import pytest


def test_importable():
    import src.cosmosdb_abstract  # noqa: F401
    from src.cosmosdb_abstract import (
        CosmosDBAbstract,  # noqa: F401
        CosmosDBConfig,  # noqa: F401
        CosmosDBMongoDBConfig,  # noqa: F401
        CosmosDBNoSQLConfig,  # noqa: F401
        CosmosDBProvider,  # noqa: F401
    )

class TestCosmosProvider:

    from src.cosmosdb_abstract import CosmosDBProvider

    @pytest.mark.parametrize("provider", [
        CosmosDBProvider.MOCKUP,
        CosmosDBProvider.COSMOSDB_NOSQL,
        CosmosDBProvider.COSMOSDB_MONGODB,
    ])
    def test_enum(self, provider):
        provider = self.CosmosDBProvider(provider)
        assert provider is not None

class TestCosmosDBAbstract:

    from src.cosmosdb_abstract import CosmosDBProvider

    @pytest.mark.parametrize("method_name", [
        "new",
        "list_databases",
        "insert",
        "isert_many",
        "find",
    ])
    def test_structure(self, method_name):
        from src.cosmosdb_abstract import CosmosDBAbstract
        assert hasattr(CosmosDBAbstract, method_name)
        assert callable(getattr(CosmosDBAbstract, method_name))

    @pytest.mark.parametrize("provider", [
        CosmosDBProvider.MOCKUP,
        CosmosDBProvider.COSMOSDB_NOSQL,
        CosmosDBProvider.COSMOSDB_MONGODB,
    ])
    def test_new(self, provider):
        from src.cosmosdb_abstract import CosmosDBAbstract
        search_engine = CosmosDBAbstract.new(provider=provider)
        assert search_engine is not None
