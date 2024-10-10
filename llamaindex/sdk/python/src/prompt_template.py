import os
import dotenv

from llama_index.core import PromptTemplate
from llama_index.llms.azure_openai import AzureOpenAI

dotenv.load_dotenv()


model = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    engine=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

# Create a prompt template
template = (
    "Answer the question in {style}."
    "{query_str}"
)
prompt_template = PromptTemplate(template)
print('=' * 16 + '\n' + 'PROMPT TEMPLATE')
print(prompt_template)

# Compile the prompt template (use format() for completion API)
messages = prompt_template.format_messages(
    style="technical details",
    query_str="who are you?"
)

# Invoke the model
response = model.chat(messages)

print('=' * 16 + '\n' + 'MODEL OUTPUT')
print(response)
