from typing import List
from llama_index.core.embeddings import BaseEmbedding


class MockupEmbedding(BaseEmbedding):
    """ Mockup embedding function for testing """

    def __init__(self):
        super().__init__()

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

    def _get_query_embedding(self, query: str) -> List[float]:
        return self._get_text_embedding(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        return [1.0 * x * len(text) for x in range(384)]

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        embeddings = []
        for doc in documents:
            embeddings.append(self._get_text_embedding(doc))
        return embeddings

    def __call__(self, input: List[str]) -> List[List[float]]:
        return self.embed_documents(input)
