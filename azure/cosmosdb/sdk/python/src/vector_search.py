import os
import logging
from typing import List

import dotenv
from azure.cosmos.cosmos_client import CosmosClient
from azure.cosmos.partition_key import PartitionKey
from azure.cosmos import exceptions

dotenv.load_dotenv()

COSMOSDB_HOST = os.getenv('COSMOSDB_HOST')
COSMOSDB_KEY = os.getenv('COSMOSDB_KEY')
COSMOSDB_DATABASE_ID = os.getenv('COSMOSDB_DATABASE_ID')
COSMOSDB_CONTAINER_NAME = os.getenv('COSMOSDB_CONTAINER_NAME')


class MockupEmbedding():
    """ Mockup embedding function for testing """

    def __init__(self):
        super().__init__()

    def query_embedding(self, query: str) -> List[float]:
        return self._get_text_embedding(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        return [1.0 * x * len(text) for x in range(384)]

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        return [self._get_text_embedding(doc) for doc in documents]

    def __call__(self, input: List[str]) -> List[List[float]]:
        return self.embed_documents(input)

# Cosmos client
cosmos_client = CosmosClient(
    COSMOSDB_HOST,
    {'masterKey': COSMOSDB_KEY},
    user_agent="CosmosDBPython",
    user_agent_overwrite=True
)

embedding = MockupEmbedding()

# Create container in the Vector store
vector_embedding_policy = {
    "vectorEmbeddings": [{
        "path": "/contentVector",
        "dataType": "float32",
        "distanceFunction": "cosine",
        "dimensions": 1536
    }]
}

indexing_policy = {
    "includedPaths": [{"path": "/*"}],
    "excludedPaths": [{
        "path": "/\"_etag\"/?",
        "path": "/contentVector/*"
    }],
    "vectorIndexes": [{
        "path": "/contentVector",
        "type": "quantizedFlat"
    }]
}

try:
    db = cosmos_client.get_database_client(COSMOSDB_DATABASE_ID)
    container = db.create_container(
        id=COSMOSDB_CONTAINER_NAME,
        partition_key=PartitionKey(path='/pkey'),
        indexing_policy=indexing_policy,
        vector_embedding_policy=vector_embedding_policy
    )
    logging.info(f"Container '{COSMOSDB_CONTAINER_NAME}' created")
except exceptions.CosmosResourceExistsError:
    container = db.get_container_client(
        container=COSMOSDB_CONTAINER_NAME
    )
    logging.info(f"Container '{COSMOSDB_CONTAINER_NAME}' found")

# Load the corpus
docs = ["foo", "bar", "baz"]

# Insert the corpus in the Vector store
for idx, doc in enumerate(docs):
    logging.info(f"Doc: {doc}")
    contentVector = embedding.embed_query(text=doc.page_content)
    container.create_item(body={
        "id": str(idx),
        "pkey": '',
        "content": doc.page_content,
        "contentVector": contentVector
    })
logging.info(f"inserted {len(docs)} documents in data store")

# Query for documents
query = 'foo'
top_k = 5
try:
    query_embedding = embedding.embed_query(query)
    db = cosmos_client.get_database_client(COSMOSDB_DATABASE_ID)
    container = db.get_container_client(COSMOSDB_CONTAINER_NAME)
    results = []
    for item in container.query_items(
        query="""
        SELECT TOP @top_k
        c.content,
        VectorDistance(c.contentVector,@embedding) AS SimilarityScore
        FROM c
        ORDER BY VectorDistance(c.contentVector,@embedding)
        """.strip(),
        parameters=[
            {"name": "@top_k", "value": top_k},
            {"name": "@embedding", "value": query_embedding},
        ],
        enable_cross_partition_query=True,
    ):
        results.append(item)
    logging.info(f"retrieved information: {results}")
except Exception as ex:
    logging.error(f"{type(ex)}: {ex}")
    logging.exception(ex)
    results = []
