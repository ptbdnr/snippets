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
embedding_func = MockupEmbedding()
vectorstore._embedding_func = embedding_func  # override attribute


# Query and retrieve data
text_retriever = ChromaQueryTextRetriever(vectorstore)
pipe = Pipeline()
pipe.add_component("text_retriever", text_retriever)
print('=' * 16 + '\n' + 'TEXT RETRIEVER OUTPUT')
print(pipe.run({"text_retriever": {"query": 'planet', "top_k": 999}}))

embedding_retriever = ChromaEmbeddingRetriever(vectorstore)
pipe = Pipeline()
pipe.add_component("embedding_retriever", embedding_retriever)
print('=' * 16 + '\n' + 'EMBEDDING RETRIEVER OUTPUT')
query_embedding = embedding_func.embed_query("What is farthest space object?")
print(pipe.run({
    "embedding_retriever": {"query_embedding": query_embedding, "top_k": 999}}
))

# Generate response
prompt_builder = PromptBuilder(template="""{{context}} {{question}}""")
embedding_retriever2 = ChromaEmbeddingRetriever(vectorstore)

rag_pipeline = Pipeline()
rag_pipeline.add_component("embedding_retriever", embedding_retriever2)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", llm)
rag_pipeline.connect("embedding_retriever", "prompt_builder.context")
rag_pipeline.connect("prompt_builder", "llm")

question = "What is farthest space object from here?"
results = rag_pipeline.run(
    {
        "embedding_retriever": {
            "query_embedding": query_embedding,
            "top_k": 999
        },
        "prompt_builder": {"question": question},
    }
)

print('=' * 16 + '\n',
      'PIPELINE OUTPUT (PROMPT -> RETRIEVER -> PROMPT_TEMPLATE -> LLM)')
print(results["llm"]["replies"][0])
