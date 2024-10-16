import os
import dotenv

from openai import AzureOpenAI

dotenv.load_dotenv()


llm = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

# Invoke the llm
messages = [
    {'role': 'system', 'content': 'Answer the question in technical details.'},
    {'role': 'user', 'content': 'who are you?'},
]

result = llm.chat.completions.create(
    model=os.environ['AZURE_OPENAI_CHAT_DEPLOYMENT_NAME'],
    messages=messages
)

print('=' * 16 + '\n' + 'LLM OUTPUT')
print(result.choices[0].message.content)
