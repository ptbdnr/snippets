import os
import dotenv

from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.llms import ChatMessage

dotenv.load_dotenv()


llm = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    engine=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

messages = [
    ChatMessage(
        role="system",
        content="Answer the question in technical details."
    ),
    ChatMessage(role="user", content="who are you?"),
]

# Invoke the LLM
response = llm.chat(messages)

print("=" * 16 + "\n" + "LLM OUTPUT")
print(response)
