import os
from dataclasses import asdict

import dotenv
import pymongo

from cosmosdb_mongodb import CosmosDBMongoDB, CosmosDBMongoDBConfig
from cosmosdb_nosql import CosmosDBNoSQL, CosmosDBNoSQLConfig

dotenv.load_dotenv()

COSMOSDB_KEY = os.getenv("COSMOSDB_KEY", "")
COSMOSDB_HOST = os.getenv("COSMOSDB_HOST", "")
COSMOSDB_DATABASE_ID = os.getenv("COSMOSDB_DATABASE_ID", "")
COSMOSDB_CONTAINER_NAME = os.getenv("COSMOSDB_CONTAINER_NAME", "")


class MockupEmbedding:
    """Mockup embedding function for testing."""

    dimensions = 384
    distance_function = "cosine"
    data_type = "float32"

    def __init__(self):
        """Initialize."""
        super().__init__()

    def query_embedding(self, query: str) -> list[float]:
        """Embed a query."""
        return self._get_text_embedding(query)

    def _get_text_embedding(self, text: str) -> list[float]:
        """Get text embedding."""
        return [1.0 * x * len(text) for x in range(self.dimensions)]

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """Embed documents."""
        return [self._get_text_embedding(doc) for doc in documents]

    def __call__(self, input: list[str]) -> list[list[float]]:
        """Embed documents."""
        return self.embed_documents(input)

vector_property_name = "contentVector"
embedding = MockupEmbedding()

# Cosmos NoSQL (enable functionality)
config = CosmosDBNoSQLConfig(
    host=COSMOSDB_HOST,
    key=COSMOSDB_KEY,
    database_id=COSMOSDB_DATABASE_ID,
    container_id=COSMOSDB_CONTAINER_NAME,
    partition_key="/pkey",
)
cosmos_client: CosmosDBNoSQL = CosmosDBNoSQL(**asdict(config))

vector_embedding_policy = {
    "vectorEmbeddings": [{
        "path": "/" + vector_property_name,
        "dataType": embedding.data_type,
        "distanceFunction": embedding.distance_function,
        "dimensions": int(embedding.dimensions),
    }],
}

indexing_policy = {
    "includedPaths": [{"path": "/*"}],
    "excludedPaths": [{
        "path": '/"_etag"/?',
        "path": "/" + vector_property_name + "/*",
    }],
    "vectorIndexes": [{
        "path": "/" + vector_property_name,
        "type": "quantizedFlat",  # one of ['flat', 'quantizedFlat', 'DiscANN']
    }],
}

container = cosmos_client.db.create_container(
    id=COSMOSDB_CONTAINER_NAME,
    partition_key="/pkey",
    indexing_policy=indexing_policy,
    vector_embedding_policy=vector_embedding_policy,
    offer_throughput=5,  # read unit count
)

item = {"id": "1", "pkey": "1", "content": "Paris is the capital of France."}
cosmos_client.insert(payload=item)
print(cosmos_client.find({}))

content_vector = embedding.query_embedding(query=item["content"])
cosmos_client.insert(payload={
    **item,
    vector_property_name: content_vector,
})

query = "foo"
top_k = 5
query_embedding = embedding.query_embedding(query=query)
query="""
SELECT TOP @top_k c.content, VectorDistance(c.contentVector,@embedding) AS SimilarityScore
FROM c
ORDER BY VectorDistance(c.contentVector,@embedding)
""".strip()
parameters=[
    {"name": "@top_k", "value": top_k},
    {"name": "@embedding", "value": query_embedding},
]
results = cosmos_client.query_items(query=query, parameters=parameters)
print(results)

# Cosmos MongoDB vCore (M40+ tier, enable functionality)
config = CosmosDBMongoDBConfig(
    host=COSMOSDB_HOST,
    key=COSMOSDB_KEY,
    database_id=COSMOSDB_DATABASE_ID,
    collection_id=COSMOSDB_CONTAINER_NAME,
)
cosmos_client: CosmosDBMongoDB = CosmosDBMongoDB(**asdict(config))

cosmos_client.create_collection_indices(
    indices=[
        {"key": [("content", pymongo.TEXT)]},
    ],
)
cosmos_client.create_vector_index(
    index_name="vector_index",
    vector_field_name=vector_property_name,
    dimensions=embedding.dimensions,
    similarity_function=embedding.distance_function,
)

item = {"_id": "1", "content": "Paris is the capital of France."}
cosmos_client.insert(payload=item)
print(cosmos_client.find({}))

content_vector = embedding.query_embedding(query=item["content"])
cosmos_client.insert_many(payloads=[{
    **item,
    vector_property_name: content_vector,
}])

query = "foo"
top_k = 5
query_embedding = embedding.query_embedding(query=query)
results = cosmos_client.vector_search(
    vector_field_name=vector_property_name,
    query_vector=query_embedding,
    top_k=top_k,
)
print(results)
