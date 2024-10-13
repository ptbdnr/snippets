import os
import dotenv
import json 
from datetime import datetime, timedelta

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


def x_hours_ahead(offset: int) -> str:
    """Return the time x hours ahead."""
    new_date = datetime.now() + timedelta(hours=offset)
    return new_date.strftime("%H:%M:%S")


# Invoke the model
result = chat_llm.run([ChatMessage.from_user("What is the date in 2 days?")])
print('=' * 16 + '\n' + 'MODEL OUTPUT WITHOUT TOOL')
print(result)

result = chat_llm.run([ChatMessage.from_user("What is the time in 2 hours?")])
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
    },
    {
        "type": "function",
        "function": {
            "name": "x_hours_ahead",
            "description": "Get the time x hours ahead.",
            "parameters": {
                "type": "object",
                "properties": {
                    "offset": {
                        "type": "number",
                        "description": "The number of hours to look ahead.",
                    },
                },
                "required": ["offset"],
            },
        }
    }
]

messages = [ChatMessage.from_user("What is the datetime in 2 days and 2 hours?")]
result = chat_llm.run(
    messages=messages,
    generation_kwargs={"tools": tools}
)
print('=' * 16 + '\n' + 'MODEL OUTPUT WITH TOOL BINDING')
print(result)

tools_map = {
    'x_days_ahead': x_days_ahead,
    'x_hours_ahead': x_hours_ahead
}
contents = json.loads(result['replies'][0].content)
for content in contents:
    fun_call = content.get('function')
    fun_name = fun_call.get('name')
    fun_args = json.loads(fun_call.get('arguments'))
    fun = tools_map.get(fun_name, None)
    if fun:
        fun_msg = ChatMessage.from_function(
            content=fun(**fun_args),
            name=fun_name
        )
        print(fun_msg)
        messages.append(fun_msg)

result = chat_llm.run(messages=messages)
print(result)
