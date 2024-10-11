import os

import dotenv

from haystack import Pipeline
from haystack.components.generators import AzureOpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder

dotenv.load_dotenv()


llm = AzureOpenAIGenerator(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

# Create a prompt template
prompt_template = """
Answer the question in {{ style }}.
{{ text }}
"""

# Create a pipeline
pipe = Pipeline()
pipe.add_component("prompt_builder", PromptBuilder(template=prompt_template))
pipe.add_component("llm", llm)
pipe.connect("prompt_builder", "llm")

# Invoke the pipeline
result = pipe.run({
    "prompt_builder": {
        "style": "technical details",
        "text": "Who are you?"
    }
})

print('=' * 16 + '\n' + 'PIPELINE OUTPUT (PROMPT -> PROMPT_BUILDER -> LLM)')
print(result)

# Parse the llm output
print('=' * 16 + '\n' + 'PARSED OUTPUT')
answer = result['llm']['replies'][0]
print(answer)

# Print the pipeline
pipe.draw(path='./prompt_template.png')
