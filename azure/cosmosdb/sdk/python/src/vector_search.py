import os
import logging
from typing import List

import dotenv
from azure.cosmos.cosmos_client import CosmosClient

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
