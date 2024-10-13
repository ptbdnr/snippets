import os
import json
from datetime import datetime, timedelta

import dotenv

from openai import AzureOpenAI

dotenv.load_dotenv()


chat_llm = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
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

result = chat_llm.chat.completions.create(
    model=os.environ['AZURE_OPENAI_CHAT_DEPLOYMENT_NAME'],
    messages=[{
        'role': 'user',
        'content': "What is the date in 2 days?"
    }]
)
print('=' * 16 + '\n' + 'MODEL OUTPUT WITHOUT TOOL')
print(result.choices[0].message.content)

result = chat_llm.chat.completions.create(
    model=os.environ['AZURE_OPENAI_CHAT_DEPLOYMENT_NAME'],
    messages=[{
        'role': 'user',
        'content': "What is the time in 2 hours?"
    }]
)
print(result.choices[0].message.content)

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

messages = [{
    'role': 'user',
    'content': "What is the datetime in 2 days and 2 hours?"
}]

result = chat_llm.chat.completions.create(
    model=os.environ['AZURE_OPENAI_CHAT_DEPLOYMENT_NAME'],
    messages=messages,
    tools=tools
)
print('=' * 16 + '\n' + 'MODEL OUTPUT WITH TOOL BINDING')
print(result)

tools_map = {
    'x_days_ahead': x_days_ahead,
    'x_hours_ahead': x_hours_ahead
}
tool_calls = result.choices[0].message.tool_calls
for tool_call in tool_calls:
    fun_call = tool_call.function
    fun_name = fun_call.name
    fun_args = json.loads(fun_call.arguments)
    fun = tools_map.get(fun_name, None)
    if fun:
        fun_msg = {
            'role': 'function',
            'name': fun_name,
            'content': fun(**fun_args),
        }
        print(fun_msg)
        messages.append(fun_msg)

result = chat_llm.chat.completions.create(
    model=os.environ['AZURE_OPENAI_CHAT_DEPLOYMENT_NAME'],
    messages=messages
)
print(result.choices[0].message.content)
