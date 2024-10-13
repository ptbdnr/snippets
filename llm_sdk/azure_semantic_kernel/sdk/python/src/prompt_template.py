import os
import asyncio

import dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.prompt_template import InputVariable, PromptTemplateConfig
from semantic_kernel.functions import KernelArguments

dotenv.load_dotenv()


kernel = Kernel()  # Initialize the kernel

service_id = 'chat-gpt'
llm = AzureChatCompletion(
    service_id=service_id,
    # base_url=os.environ["AZURE_OPENAI_ENDPOINT"],  # bug
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    deployment_name=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)
kernel.add_service(llm)

# Create a prompt template
prompt_template = """Answer the question in {{$style}}. {{$text}}"""

# Compile the prompt template
prompt_template_config = PromptTemplateConfig(
    template=prompt_template,
    name="asnwer_question_template",
    template_format="semantic-kernel",
    input_variables=[
        InputVariable(
            name="style",
            description="The requested style",
            is_required=True
        ),
        InputVariable(
            name="text",
            description="The user input text",
            is_required=True
        ),
    ],
    execution_settings=kernel.get_prompt_execution_settings_from_service_id(
        service_id=service_id
    )
)
aswer_question = kernel.add_function(
    function_name="answer_question_function",
    plugin_name="answer_question_plugin",
    prompt_template_config=prompt_template_config,
)


async def main(kernel: Kernel):

    # Invoke the LLM
    result = await kernel.invoke(
        function=aswer_question,
        arguments=KernelArguments(
            style="technical details",
            text="who are you?"
        )
    )

    print('=' * 16 + '\n' + 'LLM OUTPUT')
    print(str(result))


# Run the main function
if __name__ == "__main__":
    asyncio.run(main(kernel))
