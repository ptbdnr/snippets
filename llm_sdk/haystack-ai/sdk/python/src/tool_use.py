import os
import json
from datetime import datetime, timedelta

import dotenv

from haystack.components.generators.chat import AzureOpenAIChatGenerator
from haystack.dataclasses import ChatMessage

dotenv.load_dotenv()


chat_llm = AzureOpenAIChatGenerator(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)


def x_days_ahead(offset: int) -> str:
    """Return the date x days ahead."""
    new_date = datetime.now() + timedelta(days=offset)
    return new_date.strftime("%Y-%m-%d")


# Invoke the model

result = chat_llm.run([ChatMessage.from_user("What is the date in 2 days?")])
print('=' * 16 + '\n' + 'MODEL OUTPUT WITHOUT TOOL')
print(result)


# Add tool to the model
tools = [
    {
        "type": "function",
        "function": {
            "name": "x_days_ahead",
            "description": "Get the date x days ahead.",
            "parameters": {
                "type": "object",
                "properties": {
                    "offset": {
                        "type": "number",
                        "description": "The number of days to look ahead.",
                    },
                },
                "required": ["offset"],
            },
        }
    }
]

messages = [ChatMessage.from_user("What is the date in 2 days?")]
result = chat_llm.run(
    messages=messages,
    generation_kwargs={"tools": tools}
)
print('=' * 16 + '\n' + 'MODEL OUTPUT WITH TOOL BINDING')
print(result)

contents = json.loads(result['replies'][0].content)
for content in contents:
    fun_call = content.get('function')
    fun_name = fun_call.get('name')
    fun_args = json.loads(fun_call.get('arguments'))
    if fun_name == 'x_days_ahead':
        fun_msg = ChatMessage.from_function(
            content=x_days_ahead(**fun_args),
            name=fun_name
        )
        print(fun_msg)
        messages.append(fun_msg)

result = chat_llm.run(messages=messages)
print(result)
