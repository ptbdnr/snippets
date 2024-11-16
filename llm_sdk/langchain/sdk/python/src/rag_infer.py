## Outline
# 1: Create the LLM instance
# 2: Connect to the vector store
# 3: Create the prompt template / message list
# 4: Retrieve information and generate response
# 5: Return the result to the client

import os
import dotenv

from langchain import hub
from langchain_chroma import Chroma
from langchain_core.runnables import (
    RunnableLambda,
    RunnablePassthrough
)
from langchain_openai import AzureChatOpenAI

from mockup_embedding import MockupEmbedding

dotenv.load_dotenv()

# constants
CHROMA_PESIST_DIR_PATH = "./chroma_cache"
CHROMA_COLLECTION_NAME = "<ADD_COLLECTION_NAME>"


# Create the LLM instance
llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

# Create the Embedding client
embedding = MockupEmbedding()

# Create Vector store client
vectorstore = Chroma(
    persist_directory=CHROMA_PESIST_DIR_PATH,
    collection_name=CHROMA_COLLECTION_NAME,
    embedding_function=embedding
)

# Query and retrieve data
retriever = vectorstore.as_retriever(k=999)
prompt_template = hub.pull("rlm/rag-prompt")

print('=' * 16 + '\n' + 'PROMPT TEMPLATE')
print(prompt_template.pretty_print())


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


print('=' * 16 + '\n' + 'RETRIEVER OUTPUT')
print(retriever.invoke("What is farthest space object from here?"))


# Generate response
rag_chain = (
    # {"context": RunnableLambda(retriever) | format_docs, "question": RunnablePassthrough()}
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt_template
    | llm
)

print('=' * 16 + '\n',
      'CHAIN OUTPUT (PROMPT -> RETRIEVER -> PROMPT_TEMPLATE -> LLM)')
print(rag_chain.invoke("What is farthest space object from here?"))
