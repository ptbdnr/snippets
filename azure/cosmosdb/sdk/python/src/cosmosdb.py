import os
import logging

from azure.cosmos.cosmos_client import CosmosClient
from azure.cosmos import exceptions
from azure.cosmos.database import DatabaseProxy
from azure.cosmos.container import ContainerProxy
from azure.cosmos.partition_key import PartitionKey

from src.data_store import DataStore
from src.encrypt import mask_key

DEFAULT_SELECT_FIELDS = ['id', 'key', 'definition']
DEFAULT_PARTITION_KEY = '/partition_key'


class CosmosDB(DataStore):

    host: str = None
    key: str = None
    database_id: str = None
    container_id: str = None
    partition_key: str = None

    client: CosmosClient = None
    db: DatabaseProxy = None
    container: ContainerProxy = None
    partition_key: str = None
    select_fields: list = None

    def __init__(
        self,
        host: str = None,
        key: str = None,
        database_id: str = None,
        container_id: str = None,
        partition_key: str = None,
        select_fields: list = None
    ):
        """
        Constructor
        @param host: CosmosDB host
        @param key: CosmosDB key
        @param database_id: CosmosDB database id
        @param container_id: CosmosDB container id
        @param partition_key: CosmosDB partition key
        @param select_fields: CosmosDB return fields
        """
        logging.info(f"Start {type(self).__name__}().__init__ ...")

        # Configure
        self.host = host if host else os.getenv("DATA_STORE_COSMOSDB_HOST")
        self.key = key if key else os.getenv("DATA_STORE_COSMOSDB_KEY")
        self.database_id = database_id if database_id \
            else os.getenv("DATA_STORE_COSMOSDB_DATABASE_ID")
        self.container_id = container_id if container_id \
            else os.getenv("DATA_STORE_COSMOSDB_GLOSSARY_CONTAINER_ID")
        self.partition_key = partition_key if partition_key \
            else os.getenv("DATA_STORE_COSMOSDB_GLOSSARY_PARTITION_KEY")
        self.select_fields = select_fields if select_fields \
            else DEFAULT_SELECT_FIELDS

        # Log configuration
        logging.info(f"CosmosDB host: {self.host}")
        encrypted_key = mask_key(self.key, 2, -4)
        logging.info(f"CosmosDB key: {encrypted_key}")
        logging.info(f"CosmosDB database_id: {self.database_id}")
        logging.info(f"CosmosDB container_id: {self.container_id}")
        logging.info(f"CosmosDB partition_key: {self.partition_key}")
        logging.info(f"CosmosDB select_fields: {self.select_fields}")

        # Initialize the client
        self.client = CosmosClient(
            self.host,
            {'masterKey': self.key},
            user_agent="CosmosDBPython",
            user_agent_overwrite=True
        )

        try:
            # Setup database
            try:
                self.db = self.client.create_database(id=self.database_id)
                logging.info(f"Database with id '{self.database_id}' created")
            except exceptions.CosmosResourceExistsError:
                self.db = self.client.get_database_client(self.database_id)
                logging.info(f"Database with id '{self.database_id}' \
                    was found")

            # Setup container
            try:
                self.container = self.db.create_container(
                    id=self.container_id,
                    partition_key=PartitionKey(path=self.partition_key))
                logging.info(f"Container with id '{self.container_id}' \
                    created")
            except exceptions.CosmosResourceExistsError:
                self.container = self.db.get_container_client(
                    container=self.container_id
                )
                logging.info(f"Container with id '{self.container_id}' \
                    was found")
        except exceptions.CosmosHttpResponseError as ex:
            logging.error(f"CosmosHttpResponseError: {ex.message}")

        logging.info(f"Completed {type(self).__name__}().__init__")

    def insert_item(self, item: dict):
        """
        Create a record in the CosmosDB container
        @param record: record to insert
        """
        logging.info(f"Start {type(self).__name__}().insert_item ...")
        assert "id" in item, "The field 'id' is required in record."
        self.container.create_item(body=item)
        logging.info(f"Completed {type(self).__name__}().insert_item")

    def read_items(self, max_item_count: int = 1000) -> list:
        """
        Read all records
        @param max_item_count: max number of items to return
        @return: list of records
        """
        # NOTE: Use MaxItemCount on Options to control
        # how many items come back per trip to the server
        # Important to handle throttles whenever you are doing operations such
        # as this that might result in a 429 (throttled request)
        logging.info(f"Start {type(self).__name__}().read_items ...")
        logging.info('Start reading all items in a container ...')
        item_list = list(self.container.read_all_items(
            max_item_count=max_item_count))
        item_list = item_list[:max_item_count]
        if len(item_list) and self.select_fields:
            item_list = [{k: v for k, v in item.items()
                          if k in self.select_fields} for item in item_list]
        logging.info(f"Completed {type(self).__name__}().read_items. \
            Returned {item_list.__len__()} items")
        return item_list

    def query_items(self, field_name_value: dict) -> list:
        """
        Query records
        @param field_name_value: dictionary with key = field name
            and value = field value
        @return: list of records
        """
        logging.info(f"Start {type(self).__name__}().query_items ...")

        select_fields_concatenated = ",".join(
            ["c." + f for f in self.select_fields])
        where_fields_concatenated = " AND ".join(
            [f'c.{k} = "{v}"' for k, v in field_name_value.items() if len(v)])
        query = f"SELECT {select_fields_concatenated} \
            FROM c \
            WHERE {where_fields_concatenated}"

        logging.info(f"query: {query}")

        item_list = list(self.container.query_items(
            query=query,
            enable_cross_partition_query=True,
        ))
        logging.info(f"Completed {type(self).__name__}().query_items. \
            Returned {item_list.__len__()} items.")
        return item_list
