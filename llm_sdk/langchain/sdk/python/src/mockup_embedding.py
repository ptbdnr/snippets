from typing import List
from langchain.embeddings.base import Embeddings


class MockupEmbedding(Embeddings):
    """ Mockup embedding function for testing """

    def __init__(self):
        super().__init__()

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        embeddings = []
        for doc in documents:
            embeddings.append(self.embed_query(doc))
        return embeddings

    def embed_query(self, query: str) -> List[float]:
        return [x * len(query) for x in range(384)]

    def __call__(self, input: List[str]) -> List[List[float]]:
        return self.embed_documents(input)
