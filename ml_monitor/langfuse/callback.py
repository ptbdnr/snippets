import os

import dotenv

from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langfuse.callback import CallbackHandler
 

dotenv.load_dotenv('.env')

OPENAI_CHAT_ENDPOINT_URL = os.getenv('OPENAI_CHAT_ENDPOINT_URL')
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv('OPENAI_CHAT_ENDPOINT_KEY')
OPENAI_CHAT_ENDPOINT_DEPLOYMENT_NAME = os.getenv('OPENAI_CHAT_ENDPOINT_DEPLOYMENT_NAME')
OPENAI_CHAT_ENDPOINT_API_VERSION = os.getenv('OPENAI_CHAT_ENDPOINT_API_VERSION')

LANGFUSE_PUBLIC_KEY = os.getenv('LANGFUSE_PUBLIC_KEY')
LANGFUSE_SECRET_KEY = os.getenv('LANGFUSE_SECRET_KEY')
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"
 
# # your azure openai configuration
# os.environ["AZURE_OPENAI_ENDPOINT"] = "your Azure OpenAI endpoint"
# os.environ["AZURE_OPENAI_API_KEY"] = "your Azure OpenAI API key"
# os.environ["OPENAI_API_TYPE"] = "azure"
# os.environ["OPENAI_API_VERSION"] = "2023-09-01-preview"


# Initialize Langfuse handler
langfuse_handler = CallbackHandler()
langfuse_handler.auth_check()  # optional, verify your Langfuse credentials

# Initialize the LLM
llm = AzureChatOpenAI(
    azure_endpoint=OPENAI_CHAT_ENDPOINT_URL,
    azure_deployment=OPENAI_CHAT_ENDPOINT_DEPLOYMENT_NAME,
    openai_api_version=OPENAI_CHAT_ENDPOINT_API_VERSION,
)
 
# Create a prompt template
system_template = (
    "Please respond to the user's request "
    "only based on the given context. "
    "Be concise."
)
prompt_template = ChatPromptTemplate.from_messages(messages=[
    ("system", system_template), 
    ("user", "Question: {question}\nContext: {context}")
])
print('=' * 16 + '\n' + 'PROMPT TEMPLATE')
print(prompt_template.pretty_print())
 
# Chain the LLM and the prompt template, use langfuse_handler as a callback
def predict(input: dict) -> str:
    output_parser = StrOutputParser()
    chain = prompt_template | llm | output_parser
    return chain.invoke(
        input={
            "question": input['question'], 
            "context": input['context']
        },
        config={"callbacks":[langfuse_handler]}
    )

predict({
    "question": "What is the capital of France?",
    "context": "The capital of France is Paris."
})
