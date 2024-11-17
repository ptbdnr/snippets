import os

import dotenv

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langsmith import Client, evaluate
from langsmith.schemas import Example, Run


dotenv.load_dotenv('.env')

OPENAI_CHAT_ENDPOINT_URL = os.getenv('OPENAI_CHAT_ENDPOINT_URL')
OPENAI_CHAT_ENDPOINT_KEY = os.getenv('OPENAI_CHAT_ENDPOINT_KEY')
os.environ["AZURE_OPENAI_API_KEY"] = OPENAI_CHAT_ENDPOINT_KEY
OPENAI_CHAT_ENDPOINT_DEPLOYMENT_NAME = os.getenv('OPENAI_CHAT_ENDPOINT_DEPLOYMENT_NAME')
OPENAI_CHAT_ENDPOINT_API_VERSION = os.getenv('OPENAI_CHAT_ENDPOINT_API_VERSION')


# set up LangSmith environment (solution is entirely in LangChain)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"]="https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')
LANGSMITH_DATASET_URL = os.getenv('LANGSMITH_DATASET_URL')

# #################
# Initialize the LLM
llm = AzureChatOpenAI(
    azure_endpoint=OPENAI_CHAT_ENDPOINT_URL,
    azure_deployment=OPENAI_CHAT_ENDPOINT_DEPLOYMENT_NAME,
    openai_api_version=OPENAI_CHAT_ENDPOINT_API_VERSION,
)

# #################
# Create a prompt template
system_template = (
    "Respond to the user's request based on the given context. "
    "Be concise."
)
prompt_template = ChatPromptTemplate.from_messages(messages=[
    ("system", system_template), 
    ("user", "Question: {question}\nContext: {context}")
])
print('=' * 16 + '\n' + 'PROMPT TEMPLATE')
print(prompt_template.pretty_print())


# #################
# Chain the LLM and the prompt template
def predict(input: dict) -> str:
    output_parser = StrOutputParser()
    chain = prompt_template | llm | output_parser
    return chain.invoke({
        "question": input['question'], 
        "context": input['context']
    })

# Define the evaluator
def custom_evaluator(root_run: Run, example: Example):
    expected_output = example.outputs['output']
    prediction = root_run.outputs['output']
    return {
        "output": prediction,
        "score": 100 if expected_output == prediction else 0
    }


# Evaluate the chain output on each example in the dataset
client = Client()
dataset = client.clone_public_dataset(LANGSMITH_DATASET_URL)

evaluate(
    lambda x: predict(x),
    data=dataset.name,
    evaluators=[custom_evaluator],
    experiment_prefix="experiment_",
)