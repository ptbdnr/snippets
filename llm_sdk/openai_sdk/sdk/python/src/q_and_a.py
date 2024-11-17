import os
import json
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

# Parse the LLM output
print(f"id {result.id}")
print(f"created {result.created}")
print(f"model {result.model}")
print(f"choices {result.choices}")

for choice in result.choices:
    print(json.dumps({
        "index": choice.index,
        "finish_reason": choice.finish_reason,
        "message.role": choice.message.role,
        "message.content": choice.message.content,
        "message.tool_calls": choice.message.tool_calls
    }, indent=2))

print(f"usage {result.usage}")
print(f"prompt_tokens {result.usage.prompt_tokens}")
print(f"completion_tokens {result.usage.completion_tokens}")
print(f"total_tokens {result.usage.total_tokens}")
