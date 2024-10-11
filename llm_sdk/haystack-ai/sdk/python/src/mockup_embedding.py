from typing import List, Any, Dict
from haystack import component


class MockupEmbedding():
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

    @component.output_types(embedding=List[float], meta=Dict[str, Any])
    def run(self, text: str):
        return self.__call__(["mock embedding text"])
