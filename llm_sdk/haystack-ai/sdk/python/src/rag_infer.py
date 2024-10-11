import os
import dotenv

from haystack import Pipeline
from haystack.components.generators import AzureOpenAIGenerator
from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack_integrations.components.retrievers.chroma import (
    ChromaQueryTextRetriever,
    ChromaEmbeddingRetriever
)
from haystack.components.builders.prompt_builder import PromptBuilder

from mockup_embedding import MockupEmbedding

dotenv.load_dotenv()

# constants
CHROMA_PESIST_DIR_PATH = "./chroma_cache"
CHROMA_COLLECTION_NAME = "my_collection_d9093"


llm = AzureOpenAIGenerator(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)


vectorstore = ChromaDocumentStore(
    persist_path=CHROMA_PESIST_DIR_PATH,
    collection_name=CHROMA_COLLECTION_NAME,
)
embedding_function = MockupEmbedding()
vectorstore._embedding_func = embedding_function  # override attribute


# Query and retrieve data
pipe = Pipeline()
pipe.add_component("text_retriever", ChromaQueryTextRetriever(vectorstore))
print('=' * 16 + '\n' + 'TEXT RETRIEVER OUTPUT')
print(pipe.run({"text_retriever": {"query": 'planet', "top_k": 999}}))

pipe = Pipeline()
pipe.add_component("embedding_retriever", ChromaEmbeddingRetriever(vectorstore))
print('=' * 16 + '\n' + 'EMBEDDING RETRIEVER OUTPUT')
query_embedding = embedding_function.embed_query("What is farthest space object?")
print(pipe.run({"embedding_retriever": {"query_embedding": query_embedding, "top_k": 999}}))

# Generate response
prompt_builder = PromptBuilder(template="""{{context}} {{question}}""")

rag_pipeline = Pipeline()
rag_pipeline.add_component("embedding_retriever", ChromaQueryTextRetriever(vectorstore))
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", llm)
rag_pipeline.connect("embedding_retriever", "prompt_builder.context")
rag_pipeline.connect("prompt_builder", "llm")

question = "What is farthest space object from here?"
results = rag_pipeline.run(
    {
        "embedding_retriever": {"query": question},
        "prompt_builder": {"question": question},
    }
)

print(results["llm"]["replies"])
