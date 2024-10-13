from typing import List
from numpy import ndarray


class MockupEmbedding:
    """ Mockup embedding function for testing """
    service_id: str

    def __init__(self, service_id: str = None):
        super().__init__()
        self.service_id = service_id

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        embeddings = []
        for doc in documents:
            embeddings.append(self.embed_query(doc))
        return embeddings

    def embed_query(self, query: str) -> ndarray:
        arr = ndarray(shape=(384,), dtype=float)
        for i in range(384):
            arr[i] = i * len(query)
        return arr

    async def generate_embeddings(self, input: List[str]) -> List[List[float]]:
        return self.embed_documents(input)

    def __call__(self, input: List[str]) -> List[List[float]]:
        return self.embed_documents(input)
