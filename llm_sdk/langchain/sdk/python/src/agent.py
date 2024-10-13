import os
import dotenv
from datetime import datetime, timedelta

from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent


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

# add tools to the model
# prompt_template mush include variables "agent_scratchpad" and "input"
prompt_template = hub.pull("hwchase17/openai-tools-agent")
print('=' * 16 + '\n' + 'PROMPT TEMPLATE')
print(prompt_template.pretty_print())

tools = [x_days_ahead, x_hours_ahead]
agent = create_tool_calling_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = agent_executor.invoke({
    "input": "What is the datetime in 2 days and 2 hours?"
})
print('=' * 16 + '\n' + 'AGENT OUTPUT WITH TOOL BINDING')
print(result)
