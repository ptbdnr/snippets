import dotenv
import uuid

import chromadb
from mockup_embedding import MockupEmbedding


dotenv.load_dotenv()


# constants
CHROMA_PESIST_DIR_PATH = "./chroma_cache"
CHROMA_COLLECTION_NAME = f"my_collection_{uuid.uuid4().hex[:5]}"


chroma_client = chromadb.PersistentClient(path=CHROMA_PESIST_DIR_PATH)
new_collection = chroma_client.create_collection(
    name=CHROMA_COLLECTION_NAME,
    embedding_function=MockupEmbedding()
)
# IF embedding_function is None, THEN download all-MiniLM-L6-v2 (79.3MB)
# and cache it in ~/.cache/chroma/onnx_models

new_collection.add(
    documents=[
        "The planet BlueHeaven is 999 billion light-years away from Earth, " +
        "it is crazy blue and incredibly far. We haven't found it yet.",
        "The fruit GreyMelow in the most accid fruit in the world, " +
        "it is also the rarest. There was never any of it.",
    ],
    ids=["id1", "id2"]
)

print("CROMADB COLLECTIONS")
print(chroma_client.list_collections())

# load from disk
old_collection = chroma_client.get_collection(name=CHROMA_COLLECTION_NAME)

results = old_collection.query(
    query_texts=['mock embedding text'],  # What is farthest space object?
    n_results=1
)

print(results)
