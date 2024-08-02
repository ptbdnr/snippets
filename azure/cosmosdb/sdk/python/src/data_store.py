from abc import ABC, abstractmethod
from enum import Enum


class DataStoreProvider(Enum):
    """
    Enum for data store provider.
    """
    MOCKUP = "mockup"
    COSMOSDB = "cosmosdb"


class DataStore(ABC):
    """
    Abstract class for data store.
    """

    @staticmethod
    def new(provider: DataStoreProvider, data_store_config: dict = None):
        if provider == DataStoreProvider.MOCKUP:
            from src.mockup_data_store import MockupDataStore
            return MockupDataStore()
        elif provider == DataStoreProvider.COSMOSDB:
            from src.cosmosdb import CosmosDB
            return CosmosDB(**data_store_config) if data_store_config \
                else CosmosDB()
        else:
            raise ValueError(f"Invalid provider: {provider}")

    @abstractmethod
    def insert_item(self, item: dict):
        raise NotImplementedError

    @abstractmethod
    def read_items(self, max_item_count: int) -> list:
        raise NotImplementedError

    @abstractmethod
    def query_items(self, field_name_value: dict) -> list:
        raise NotImplementedError
