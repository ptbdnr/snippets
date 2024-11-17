import os

import dotenv

from openai import AzureOpenAI

dotenv.load_dotenv('.env')

openai_client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

messages = [{'role': 'user', 'content': 'Who are you? Be concise.'}]

response = openai_client.chat.completions.create(
    model=os.environ['AZURE_OPENAI_CHAT_DEPLOYMENT_NAME'],
    messages=messages,
    stream=True
)
for chunk in response:
    msg = f"created: {chunk.created}"
    for choice in chunk.choices:
        msg += f" choice: {choice.index}"
        msg += f" finish_reason: {choice.finish_reason}"
        msg += f" delta.content: \"{choice.delta.content}\""
    print(msg)
