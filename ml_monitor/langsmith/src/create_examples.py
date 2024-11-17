import os

import dotenv

from langsmith import Client

dotenv.load_dotenv('.env')

# set up LangSmith environment (solution is entirely in LangChain)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

# Initialize the LangSmith client
ls_client = Client()

dataset_name = "example_dataset"
dataset = ls_client.create_dataset(
    dataset_name, 
    description="Example dataset for LangSmith"
)

inputs = []
outputs = []

ls_client.create_examples(
    dataset_id=dataset.id,
    inputs=inputs,
    outputs=outputs,
)