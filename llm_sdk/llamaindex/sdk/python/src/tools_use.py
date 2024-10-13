import os
import dotenv
from datetime import datetime, timedelta

from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent

dotenv.load_dotenv()


llm = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    engine=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
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


tool_x_days_ahead = FunctionTool.from_defaults(fn=x_days_ahead)
tool_x_hours_ahead = FunctionTool.from_defaults(fn=x_hours_ahead)

print('=' * 16 + '\n' + 'TOOL OUTPUT (2 day ahead)')
print(tool_x_days_ahead(offset=2))

print('=' * 16 + '\n' + 'TOOL OUTPUT (2 hours ahead)')
print(tool_x_hours_ahead(offset=2))

# Invoke the model
messages = [ChatMessage(role="user", content="What is the date in 2 days?")]
result = llm.chat(messages=messages)
print('=' * 16 + '\n' + 'MODEL OUTPUT WITHOUT TOOL')
print(result)

messages = [ChatMessage(role="user", content="What is the time in 2 hours?")]
result = llm.chat(messages=messages)
print(result)


# Add tools to the model
tools = [tool_x_days_ahead, tool_x_hours_ahead]
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True)

result = agent.chat("What is the datetime in 2 days and 2 hours?")
print('=' * 16 + '\n' + 'MODEL OUTPUT WITH TOOL BINDING')
print(result)
