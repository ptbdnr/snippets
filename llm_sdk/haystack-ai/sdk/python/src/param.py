import os

import dotenv

from haystack.components.generators.chat import AzureOpenAIChatGenerator
from haystack.dataclasses import ChatMessage

dotenv.load_dotenv()


chat_llm = AzureOpenAIChatGenerator(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)


messages = [
    ChatMessage.from_system("Answer the question in technical details."),
    ChatMessage.from_user("who are you?"),
]

# Invoke the LLM
result = chat_llm.run(messages=messages)
print('=' * 16 + '\n' + 'LLM OUTPUT')
print(result)

# Parse the LLM output
print('=' * 16 + '\n' + 'PARSED OUTPUT')
answer = result['replies'][0].content
print(answer)
