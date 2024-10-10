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


tool = FunctionTool.from_defaults(fn=x_days_ahead)

print('=' * 16 + '\n' + 'TOOL OUTPUT (2 day ahead)')
print(tool(offset=2))

# Invoke the model
messages = [ChatMessage(role="user", content="What is the date in 2 days?")]
result = llm.chat(messages=messages)
print('=' * 16 + '\n' + 'MODEL OUTPUT WITHOUT TOOL')
print(result)

# add tool to the model
agent = ReActAgent.from_tools([tool], llm=llm, verbose=True)

result = agent.chat("What is the date in 2 days?")
print('=' * 16 + '\n' + 'MODEL OUTPUT WITH TOOL BINDING')
print(result)
