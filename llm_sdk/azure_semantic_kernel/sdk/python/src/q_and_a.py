import os
import asyncio

import dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.prompt_execution_settings import (
    PromptExecutionSettings
)
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

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
req_settings = kernel.get_prompt_execution_settings_from_service_id(service_id)


async def main(kernel: Kernel, req_settings: PromptExecutionSettings):
    messages = ChatHistory()
    messages.add_system_message("Answer the question in technical details.")
    messages.add_user_message("who are you?")

    # Invoke the LLM
    result = await llm.get_chat_message_content(
        chat_history=messages,
        kernel=kernel,
        settings=req_settings,
    )

    print('=' * 16 + '\n' + 'LLM OUTPUT')
    print(str(result))


# Run the main function
if __name__ == "__main__":
    asyncio.run(main(kernel, req_settings))
