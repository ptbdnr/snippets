import os
import dotenv

from openai import AzureOpenAI

dotenv.load_dotenv()


llm = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

# Create a prompt template
template = """
    Answer the question in {style}.
    {query_str}
""".strip()

# Compile the prompt template
messages = [{
    'role': 'user',
    'content': template.format(style="technical details", query_str="who are you?")
}]

# Invoke the llm
result = llm.chat.completions.create(
    model=os.environ['AZURE_OPENAI_CHAT_DEPLOYMENT_NAME'],
    messages=messages
)

print('=' * 16 + '\n' + 'LLM OUTPUT')
print(result.choices[0].message.content)
