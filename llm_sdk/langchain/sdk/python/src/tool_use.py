import os
import dotenv
from datetime import datetime, timedelta

from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool


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


print('=' * 16 + '\n' + 'TOOL OUTPUT (2 day ahead)')
print(x_days_ahead.invoke({"offset": 2}))

# Invoke the model
result = llm.invoke("What is the date in 2 days?")
print('=' * 16 + '\n' + 'MODEL OUTPUT WITHOUT TOOL')
print(result)


# Add tool to the model
llm_with_tools = llm.bind_tools([x_days_ahead])

result = llm_with_tools.invoke("What is the date in 2 days?")
print('=' * 16 + '\n' + 'MODEL OUTPUT WITH TOOL BINDING')
print(result)

print('=' * 16 + '\n' + 'CHAIN OUTPUT (MODEL -> TOOL)')
chain = llm_with_tools | (lambda x: x.tool_calls[0]["args"]) | x_days_ahead
print(chain.invoke("What is the date in 2 days?"))
