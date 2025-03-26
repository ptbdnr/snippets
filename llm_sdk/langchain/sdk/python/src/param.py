import os
import dotenv

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_community.callbacks import get_openai_callback
from langchain_core.messages import AIMessage

dotenv.load_dotenv()


llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

messages = [
    SystemMessage(content="Answer the question in technical details."),
    HumanMessage(content="who are you?"),
]

# Invoke the llm
result = llm.invoke(messages)

print('=' * 16 + '\n' + 'LLM OUTPUT')
print(result)

# Parse the LLM output
parser = StrOutputParser()

answer = parser.invoke(result)

print('=' * 16 + '\n' + 'PARSED OUTPUT')
print(answer)

# Chain the LLM and the parser
chain = llm | parser

print('=' * 16 + '\n' + 'CHAIN OUTPUT (MESSAGES -> LLM -> PARSER)')

with get_openai_callback() as cb:
    result: AIMessage = chain.invoke(messages)
    print(f"ai message: {result}")

# get input token count
print(f"input tokens: {cb.prompt_tokens}")
