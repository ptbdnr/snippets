from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Optional


class CosmosDBProvider(Enum):
    """Enum for data store provider."""

    MOCKUP = "mockup"
    COSMOSDB_NOSQL = "cosmosdb_nosql"
    COSMOSDB_MONGODB = "cosmosdb_mongodb"

@dataclass
class CosmosDBConfig:
    """CosmosDB configuration."""

class CosmosDBAbstract(ABC):
    """Abstract class for data store."""

    @staticmethod
    def new(
        provider: CosmosDBProvider,
        config: Optional[CosmosDBConfig],
    ) -> "CosmosDBAbstract":
        """Create a new data store."""
        if provider == CosmosDBProvider.MOCKUP:
            from src.cosmosdb_mockup import CosmosDBMockup
            return CosmosDBMockup()
        if provider == CosmosDBProvider.COSMOSDB_NOSQL:
            from src.cosmosdb_nosql import CosmosDBNoSQL
            if not config:
                msg = "Config is required for CosmosDBNoSQL"
                raise ValueError(msg)
            return CosmosDBNoSQL(**asdict(config))
        if provider == CosmosDBProvider.COSMOSDB_MONGODB:
            from src.cosmosdb_mongodb import CosmosDBMongoDB
            if not config:
                msg = "Config is required for CosmosDBMongoDB"
                raise ValueError(msg)
            return CosmosDBMongoDB(**asdict(config))
        msg = f"Invalid provider: {provider}"
        raise ValueError(msg)

    @abstractmethod
    def list_databases(self) -> list:
        """List databases."""
        raise NotImplementedError

    @abstractmethod
    def insert(self, payload: dict) -> dict:
        """Insert a payload."""
        raise NotImplementedError

    @abstractmethod
    def insert_many(self, payloads: list[dict]) -> list:
        """Insert many payloads."""
        raise NotImplementedError

    @abstractmethod
    def find(self, filter: Optional[dict]) -> list:
        """Find items."""
        raise NotImplementedError
