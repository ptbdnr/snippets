from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from azure.cosmos import exceptions
from azure.cosmos.cosmos_client import CosmosClient
from azure.cosmos.partition_key import PartitionKey

from src.cosmosdb_abstract import CosmosDBAbstract, CosmosDBConfig

if TYPE_CHECKING:
    from azure.cosmos.container import ContainerProxy
    from azure.cosmos.database import DatabaseProxy


ALLOWED_SELECT_FIELDS = ["id", "key", "definition"]
DEFAULT_PARTITION_KEY = "/partition_key"

@dataclass
class CosmosDBNoSQLConfig(CosmosDBConfig):
    """CosmosDB configuration."""

    host: str
    key: str
    database_id: str
    container_id: str
    partition_key: str


class CosmosDBNoSQL(CosmosDBAbstract):
    """CosmosDB data store."""

    database_id: str
    container_id: str
    partition_key: str

    client: CosmosClient
    db: DatabaseProxy
    container: ContainerProxy

    def __init__(
        self,
        host: str,
        key: str,
        database_id: str,
        container_id: str,
        partition_key: str,
    ) -> None:
        """Initialize."""
        # Configure
        self.database_id = database_id
        self.container_id = container_id
        self.partition_key = partition_key if partition_key else DEFAULT_PARTITION_KEY

        # Initialize the client
        self.client = CosmosClient(
            url=host,
            credential={"masterKey": key},
            user_agent="CosmosDBPython",
            user_agent_overwrite=True,
        )

        try:
            # Setup database
            try:
                self.db = self.client.create_database(id=self.database_id)
            except exceptions.CosmosResourceExistsError:
                self.db = self.client.get_database_client(database=self.database_id)

            # Setup container
            try:
                self.container = self.db.create_container(
                    id=self.container_id,
                    partition_key=PartitionKey(path=self.partition_key))
            except exceptions.CosmosResourceExistsError:
                self.container = self.db.get_container_client(
                    container=self.container_id,
                )
        except exceptions.CosmosHttpResponseError as ex:
            print(f"CosmosHttpResponseError: {ex.message}")

    def list_databases(self) -> list:
        """List databases."""
        return list(self.client.list_databases())

    def insert(self, payload: dict) -> dict:
        """Insert a payload."""
        if "id" not in payload:
            msg = "The field 'id' is required in record."
            raise ValueError(msg)
        return self.container.create_item(body=payload)

    def insert_many(self, payloads: list[dict]) -> list:
        """Insert many payloads."""
        return [self.insert(payload) for payload in payloads]

    def read_all_items(self, max_item_count: Optional[int]) -> list:
        """Read all records."""
        # NOTE: Use MaxItemCount on Options to control
        # how many items come back per trip to the server
        # Important to handle throttles whenever you are doing operations such
        # as this that might result in a 429 (throttled request)
        return list(self.container.read_all_items(max_item_count=max_item_count))

    def query_items(self, query: str) -> list:
        """Query items."""
        return list(self.container.query_items(
            query=query,
            enable_cross_partition_query=True,
        ))

    def find(self, filter: Optional[dict]) -> list:
        """Find items."""
        validated_fields = ", ".join("c." + f for f in ALLOWED_SELECT_FIELDS)
        query = "SELECT " + validated_fields + " FROM c"
        parameters = []
        conditions = []
        if filter:
            for k, v in filter.items():
                if v:
                    param_name = f"@{k}"
                    conditions.append(f"c.{k} = {param_name}")
                    parameters.append({"name": param_name, "value": v})
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        return list(self.container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True,
        ))
