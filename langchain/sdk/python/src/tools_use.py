import os
import dotenv
from datetime import datetime, timedelta

from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable

dotenv.load_dotenv()


llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)


@tool
def x_days_ahead(offset: int) -> str:
    """Return the date x days ahead."""
    new_date = datetime.now() + timedelta(days=offset)
    return new_date.strftime("%Y-%m-%d")


@tool
def x_hours_ahead(offset: int) -> str:
    """Return the time x hours ahead."""
    new_date = datetime.now() + timedelta(hours=offset)
    return new_date.strftime("%H:%M:%S")


print('=' * 16 + '\n' + 'TOOL OUTPUT (2 day ahead)')
print(x_days_ahead.invoke({"offset": 2}))

print('=' * 16 + '\n' + 'TOOL OUTPUT (2 hours ahead)')
print(x_hours_ahead.invoke({"offset": 2}))


# Invoke the model
result = llm.invoke("What is the date in 2 days?")
print('=' * 16 + '\n' + 'MODEL OUTPUT WITHOUT TOOL')
print(result)

result = llm.invoke("What is the time in 2 hours?")
print(result)

# add tools to the model (max 1 tool will be called)


def call_tools(msg: AIMessage) -> Runnable:
    """Simple sequential tool calling helper."""
    tool_map = {tool.name: tool for tool in tools}
    tool_calls = msg.tool_calls.copy()
    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_call["output"] = tool_map[tool_name].invoke(tool_args)
    return tool_calls


tools = [x_days_ahead, x_hours_ahead]
llm_with_tools = llm.bind_tools(tools)

result = llm_with_tools.invoke("What is the date in 2 days and 2 hours?")
print('=' * 16 + '\n' + 'MODEL OUTPUT WITH TOOL BINDING')
print(result)

chain = llm_with_tools | call_tools
result = chain.invoke("What is the date in 2 days and 2 hours?")
print('=' * 16 + '\n' + 'CHAIN OUTPUT (MODEL -> TOOLS)')
print(result)
