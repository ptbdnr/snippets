## Outline
# 1: Create the LLM instance
# 2: Connect to the vector store
# 3: Create the prompt template / message list
# 4: Retrieve information and generate response
# 5: Return the result to the client

import os
import dotenv

from openai import AzureOpenAI
import chromadb
from mockup_embedding import MockupEmbedding

dotenv.load_dotenv()

# constants
CHROMA_PESIST_DIR_PATH = "./chroma_cache"
CHROMA_COLLECTION_NAME = "my_collection_996d6"  # f"<ADD_COLLECTION_NAME>"


llm = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

chroma_client = chromadb.PersistentClient(path=CHROMA_PESIST_DIR_PATH)

# Query and retrieve data
query_str = "What is farthest space object from here?"
old_collection = chroma_client.get_collection(
    name=CHROMA_COLLECTION_NAME,
    embedding_function=MockupEmbedding()
)
results = old_collection.query(
    query_texts=[query_str],
    n_results=2
)
print('=' * 16 + '\n' + 'RETRIEVER OUTPUT')
print([doc for doc in results['documents']])


# Generate response
messages = [{
    'role': 'user',
    'content': """
        Answer the question: {query_str}
        Given the context: {context}
    """.strip().format(
        context=[[doc for doc in results['documents']]],
        query_str="What is farthest space object from here?"
    )
}]

result = llm.chat.completions.create(
    model=os.environ['AZURE_OPENAI_CHAT_DEPLOYMENT_NAME'],
    messages=messages
)

print('=' * 16 + '\n' + 'LLM OUTPUT')
print(result.choices[0].message.content)
