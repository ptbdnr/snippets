import os
import logging
import asyncio

import dotenv


from semantic_kernel import Kernel
from semantic_kernel.utils.logging import setup_logging
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_call_behavior import FunctionCallBehavior
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)

dotenv.load_dotenv()

# Initialize the kernel
kernel = Kernel()

# Add Azure OpenAI chat completion
chat_completion = AzureChatCompletion(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
)
kernel.add_service(chat_completion)

# Set the logging level for  semantic_kernel.kernel to DEBUG.
setup_logging()
logging.getLogger("kernel").setLevel(logging.DEBUG)

# Add a plugin (the LightsPlugin class is defined below)
kernel.add_plugin(
    LightsPlugin(),
    plugin_name="Lights",
)

# Enable planning
execution_settings = AzureChatPromptExecutionSettings(tool_choice="auto")
execution_settings.function_call_behavior = FunctionCallBehavior.EnableFunctions(auto_invoke=True, filters={})

# Create a history of the conversation
history = ChatHistory()

# Initiate a back-and-forth chat
userInput = None
while True:
    # Collect user input
    userInput = input("User > ")

    # Terminate the loop if the user says "exit"
    if userInput == "exit":
        break

    # Add user input to the history
    history.add_user_message(userInput)

    # Get the response from the AI
    result = await chat_completion.get_chat_message_content(
        chat_history=history,
        settings=execution_settings,
        kernel=kernel,
    )

    # Print the results
    print("Assistant > " + str(result))

    # Add the message from the agent to the chat history
    history.add_message(result)
