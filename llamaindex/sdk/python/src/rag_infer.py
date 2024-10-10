import os
import dotenv

import chromadb

from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex

from mockup_embedding import MockupEmbedding


dotenv.load_dotenv()

# constants
CHROMA_PESIST_DIR_PATH = "./chroma_cache"
CHROMA_COLLECTION_NAME = "my_collection_0d153"


llm = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    engine=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)


# load from disk
chroma_client = chromadb.PersistentClient(path=CHROMA_PESIST_DIR_PATH)
chroma_collection = chroma_client.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME,
    embedding_function=MockupEmbedding()
)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(
    vector_store,
    embed_model=MockupEmbedding()
)

# Query Data from the persisted index
# TODO: ValueError: "Could not load OpenAI model. If you intended to use OpenAI, please check your OPENAI_API_KEY."
query_engine = index.as_query_engine(llm=None)
response = query_engine.query("What did the author do growing up?")
print('=' * 16 + '\n' + 'RETRIEVER OUTPUT')
print(response)
