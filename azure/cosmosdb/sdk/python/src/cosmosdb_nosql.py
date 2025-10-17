from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from azure.cosmos import exceptions
from azure.cosmos.cosmos_client import CosmosClient
from azure.cosmos.partition_key import PartitionKey
from azure.identity import DefaultAzureCredential

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
        if False:
            connection_string = "nosql_connection_string"
            self.client = CosmosClient.from_connection_string(connection_string)
        elif False:
            # running in cloud
            # Auth: running in Azure host; using DefaultAzureCredential without interactive sources.
            url = config["nosql_url"]
            credential = DefaultAzureCredential(
                exclude_interactive_browser_credential=True,
                exclude_visual_studio_code_credential=True,
                exclude_shared_token_cache_credential=True,
                exclude_cli_credential=False,
                exclude_powershell_credential=True,
                exclude_developer_cli_credential=True,
            )
            self.client = CosmosClient(url=host, credential=credential)
        else:
            self.client = CosmosClient(
                url=host,
                credential={"masterKey": key},
                user_agent="CosmosDBPython",
                user_agent_overwrite=True,
            )

    def create_container(
            self,
            indexing_policy: Optional[dict] = None,
            vector_embedding_policy: Optional[dict] = None,
            offer_throughput: Optional[int] = None,
            drop_old_database: bool = False,
            drop_old_container: bool = False,
    ) -> ContainerProxy:
        """Create a container."""
        if self.client is None:
            msg = "CosmosDB client not found"
            raise ValueError(msg)
        if self.db is None:
            if drop_old_database:
                self.client.delete_database(id=self.database_id)
            try:
                self.db = self.client.create_database(id=self.database_id)
            except exceptions.CosmosResourceExistsError:
                self.db = self.client.get_database_client(database=self.database_id)
        if self.container is None:
            if drop_old_container:
                self.db.delete_container(id=self.container_id)
            try:
                self.container = self.db.create_container(
                    id=self.container_id,
                    partition_key=PartitionKey(path=self.partition_key),
                    indexing_policy=indexing_policy,
                    vector_embedding_policy=vector_embedding_policy,
                    offer_throughput=offer_throughput,
                )
            except exceptions.CosmosResourceExistsError:
                self.container = self.db.get_container_client(
                    container=self.container_id,
                )
        return self.container

    def list_databases(self) -> list:
        """List databases."""
        self.create_container()
        return list(self.client.list_databases())

    def insert(self, payload: dict) -> dict:
        """Insert a payload."""
        self.create_container()
        if "id" not in payload:
            msg = "The field 'id' is required in record."
            raise ValueError(msg)
        return self.container.create_item(body=payload)

    def insert_many(self, payloads: list[dict]) -> list:
        """Insert many payloads."""
        self.create_container()
        return [self.insert(payload) for payload in payloads]

    def read_all_items(self, max_item_count: Optional[int]) -> list:
        """Read all records."""
        self.create_container()
        # NOTE: Use MaxItemCount on Options to control
        # how many items come back per trip to the server
        # Important to handle throttles whenever you are doing operations such
        # as this that might result in a 429 (throttled request)
        return list(self.container.read_all_items(max_item_count=max_item_count))

    def query_items(
            self,
            query: str,
            parameters: Optional[list] = None,
            enable_cross_partition_query: bool = True,
    ) -> list:
        """Query items."""
        self.create_container()
        return list(self.container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=enable_cross_partition_query,
        ))

    def find(self, filter: Optional[dict]) -> list:
        """Find items."""
        self.create_container()
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
