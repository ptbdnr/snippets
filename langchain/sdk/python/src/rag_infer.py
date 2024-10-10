import os
import dotenv

from langchain import hub
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import AzureChatOpenAI

from mockup_embedding import MockupEmbedding

dotenv.load_dotenv()

# constants
CHROMA_PESIST_DIR_PATH = "./chroma_cache"
CHROMA_COLLECTION_NAME = "<ADD_COLLECTION_NAME>"


llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)


vectorstore = Chroma(
    persist_directory=CHROMA_PESIST_DIR_PATH,
    collection_name=CHROMA_COLLECTION_NAME,
    embedding_function=MockupEmbedding()
)

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever(k=999)
prompt_template = hub.pull("rlm/rag-prompt")

print('=' * 16 + '\n' + 'PROMPT TEMPLATE')
print(prompt_template.pretty_print())


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


print('=' * 16 + '\n' + 'RETRIEVER OUTPUT')
print(retriever.invoke("What is furthest space object from here?"))

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt_template
    | llm
)

print('=' * 16 + '\n' + 'CHAIN OUTPUT (RETRIEVER -> PROMPT_TEMPLATE -> MODEL)')
print(rag_chain.invoke("What is furthest space object from here?"))
