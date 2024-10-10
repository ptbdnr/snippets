import os
import dotenv

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

dotenv.load_dotenv()


model = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

messages = [
    SystemMessage(content="Answer the question in technical details."),
    HumanMessage(content="who are you?"),
]

# Invoke the model
result = model.invoke(messages)

print('=' * 16 + '\n' + 'MODEL OUTPUT')
print(result)

# Parse the model output
parser = StrOutputParser()

answer = parser.invoke(result)

print('=' * 16 + '\n' + 'PARSED OUTPUT')
print(answer)

# Chain the model and the parser
chain = model | parser

print('=' * 16 + '\n' + 'CHAIN OUTPUT (MODEL -> PARSER)')
print(chain.invoke(messages))
