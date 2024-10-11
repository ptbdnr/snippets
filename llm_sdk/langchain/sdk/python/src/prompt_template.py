import os
import dotenv

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

dotenv.load_dotenv()


llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

# Create a prompt template
system_template = "Answer the question in {style}."
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)
print('=' * 16 + '\n' + 'PROMPT TEMPLATE')
print(prompt_template.pretty_print())

# Compile the prompt template
pt_result = prompt_template.invoke({
    "style": "technical details",
    "text": "who are you?"
})
messages = pt_result.to_messages()

# Invoke the LLM
result = llm.invoke(messages)

print('=' * 16 + '\n' + 'LLM OUTPUT')
print(result)

# Chain the LLM and the prompt template
chain = prompt_template | llm
result = chain.invoke({
    "style": "technical details",
    "text": "who are you?"
})

print('=' * 16 + '\n' + 'CHAIN OUTPUT (PROMPT -> PROMPT_TEMPLATE -> LLM)')
print(result)
