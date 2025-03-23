from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional

import pymongo
from pymongo import MongoClient, ReturnDocument, database

from src.cosmosdb_abstract import CosmosDBAbstract, CosmosDBConfig

DEFAULT_SELECT_FIELDS = ["id", "key", "definition"]
DEFAULT_PARTITION_KEY = "/partition_key"

@dataclass
class CosmosDBMongoDBConfig(CosmosDBConfig):
    """CosmosDB configuration."""

    connection_string: str
    db_name: str
    collection_name: str
    index_name: str


class CosmosDBMongoDB(CosmosDBAbstract):
    """CosmosDB with MongoDB vCore."""

    db_name: str
    collection_name: str
    index_name: str

    client : MongoClient
    db: database.Database
    collection: database.Collection

    def __init__(
            self,
            connection_string: str,
            db_name: str,
            collection_name: str,
            index_name: str,
    ):
        """Initialize."""
        self.db_name = db_name
        self.collection_name = collection_name
        self.index_name = index_name

        self.client = MongoClient(connection_string)

    def create_collection(
            self,
            drop_old_database: bool = False,
            drop_old_collection: bool = False,
    ) -> database.Collection:
        """Create a collection."""
        if self.client is None:
            msg = "MongoDB client not found"
            raise ValueError(msg)
        if self.db is None:
            if drop_old_database:
                self.client.drop_database(self.db_name)
            self.db = self.client[self.db_name]
        if self.collection is None:
            collection_names = self.db.list_collection_names()
            if drop_old_collection and self.collection_name in collection_names:
                self.db.drop_collection(self.collection_name)
            if self.collection_name not in self.db.list_collection_names():
                self.db.create_collection(self.collection_name)
            self.collection = self.db[self.collection_name]
        return self.collection

    def list_databases(self) -> list:
        """List databases."""
        return self.client.list_databases()

    def create_collection_indices(
            self,
            collection_name: str,
            indices: list[tuple],
    ) -> None:
        """Create collection indices.

        Example indices: [("content_text", pymongo.TEXT)]
        """
        self.create_collection()
        if self.db is None:
            msg = "Database not found"
            raise ValueError(msg)
        collection = self.db[collection_name]
        collection.create_index(indices)

    def create_vector_index(
            self,
            index_name: str,
            vector_field_name: str,
            dimensions: int,
            similarity_function: str = "cosine",
    ) -> dict:
        """Create a vector index."""
        result = self.db.command({
            "createIndexes": self.collection_name,
            "indexes": [
                {
                    "name": index_name,
                    "key": {
                        vector_field_name: "cosmosSearch",
                    },
                    # "cosmosSearchOptions": {
                    #     "kind": "vector-ivf",
                    #     "numLists": 64,
                    #     "similarity": similarity_function,
                    #     "dimensions": dimensions,
                    # },
                    # "cosmosSearchOptions": {
                    #     "kind": "vector-hnsw",
                    #     "m": 54,
                    #     "efConstruction": 64,
                    #     "similarity": similarity_function,
                    #     "dimensions": dimensions,
                    # },
                    "cosmosSearchOptions": {
                        "kind": "vector-diskann",
                        "dimensions": dimensions,
                        "similarity": similarity_function,
                        "maxDegree": 32,
                        "lBuild": 64,
                    },
                },
                {
                    "name": "contentTextIndex",
                    "key": {
                        "content_text": 1,
                    },
                },
            ],
        })

        # Wait for initial sync to complete
        try:
            print("Polling to check if the index is ready. This may take up to a minute.")
            def predicate(index: dict) -> bool:
                return index.get("queryable") is True
            while True:
                indices = list(self.collection.list_search_indexes(name=index_name))
                if len(indices) > 0 and predicate(indices[0]):
                    break
                time.sleep(5)
        except pymongo.errors.OperationFailure as ex:
            print(ex)

        return result

    def insert(self, payload: dict) -> dict:
        """Insert a payload."""
        self.create_collection()
        if self.collection is None:
            msg = "Collection not found"
            raise ValueError(msg)
        # if payload contains an _id, use it as filter for upsert, otherwise use payload as filter
        filter = {"_id": payload["_id"]} if "_id" in payload else payload
        return self.collection.find_one_and_update(
            filter,
            {"$set": payload},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

    def insert_many(self, payloads: list[dict]) -> list:
        """Insert many payloads."""
        self.create_collection()
        if self.collection is None:
            msg = "Collection not found"
            raise ValueError(msg)
        updated_docs = []
        for payload in payloads:
            filter = {"_id": payload["_id"]} if "_id" in payload else payload
            updated_doc = self.collection.find_one_and_update(
                filter,
                {"$set": payload},
                upsert=True,
                return_document=ReturnDocument.AFTER,
            )
            updated_docs.append(updated_doc)
        return updated_docs

    def find(
        self,
        filter: Optional[dict] = None,
    ) -> list:
        """Find items."""
        self.create_collection()
        if self.collection is None:
            msg = "Collection not found"
            raise ValueError(msg)
        return self.collection.find(filter=filter)

    def vector_search(
        self,
        vector_field_name: str,
        query_vector: list,
        top_k: int,
    ) -> list:
        """Vector search."""
        self.create_collection()
        if self.collection is None:
            msg = "Collection not found"
            raise ValueError(msg)
        pipeline = [
            {
                "$search": {
                    "cosmosSearch": {
                        "path": vector_field_name,
                        "vector": query_vector,
                        "k": top_k,
                    },
                },
            },
        ]
        return list(self.collection.aggregate(pipeline))
