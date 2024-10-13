import os
import asyncio
from datetime import datetime, timedelta

import dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import (
    AzureChatCompletion,
    AzureChatPromptExecutionSettings
)
from semantic_kernel.functions import (
    kernel_function,
    KernelFunction,
    KernelPlugin,
    KernelArguments,
)
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior
)
from semantic_kernel.contents.chat_history import ChatHistory

dotenv.load_dotenv()


kernel = Kernel()  # Initialize the kernel

llm_service_id = 'chat-gpt'
llm = AzureChatCompletion(
    service_id=llm_service_id,
    # base_url=os.environ["AZURE_OPENAI_ENDPOINT"],  # bug
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    deployment_name=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)
kernel.add_service(llm)

prompt_execution_settings = kernel.\
    get_prompt_execution_settings_from_service_id(llm_service_id)


@kernel_function(
    description="Return the date x days ahead."
)
def x_days_ahead(offset: int) -> str:
    new_date = datetime.now() + timedelta(days=offset)
    return new_date.strftime("%Y-%m-%d")


custom_function = kernel.add_function(
    plugin_name="x_days_ahead",
    function=x_days_ahead,
)


class DatetimeLookAheadPlugin:
    @kernel_function(
        name='XDaysAhead',
        description="Return the date x days ahead."
    )
    def x_days_ahead(self, offset: int) -> str:
        new_date = datetime.now() + timedelta(days=offset)
        return new_date.strftime("%Y-%m-%d")


custom_plugin = kernel.add_plugin(
    plugin=DatetimeLookAheadPlugin(),
    plugin_name="DatetimeLookAhead"
)


async def main(
    kernel: Kernel,
    chat_service: AzureChatCompletion,
    custom_function: KernelFunction,
    custom_plugin: KernelPlugin
) -> None:
    pass

    result = await kernel.invoke(custom_function, offset=2)
    print('=' * 16 + '\n' + 'TOOL/FUNCTION OUTPUT (2 day ahead)')
    print(result)

    result = await custom_plugin.get('XDaysAhead').invoke(
        kernel=kernel,
        offset=2
    )
    print('=' * 16 + '\n' + 'PLUGIN OUTPUT (2 day ahead)')
    print(result)

    # Invoke the model
    messages = ChatHistory()
    messages.add_user_message("What is the date in 2 days?")

    result = await chat_service.get_chat_message_content(
        chat_history=messages,
        kernel=kernel,
        settings=kernel.get_prompt_execution_settings_from_service_id(
            service_id=chat_service.service_id
        ),
    )
    print('=' * 16 + '\n' + 'MODEL OUTPUT WITHOUT TOOL')
    print(result)

    # Allow tool to the model
    execution_settings = AzureChatPromptExecutionSettings(tool_choice="auto")
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto(
        filters={"included_plugins": ["DatetimeLookAhead"]}
    )
    result = await chat_service.get_chat_message_contents(
        chat_history=messages,
        settings=execution_settings,
        kernel=kernel,
        arguments=KernelArguments(),
    )
    print('=' * 16 + '\n' + 'MODEL OUTPUT WITH TOOL BINDING')
    print(result[0])


# Run the main function
if __name__ == "__main__":
    asyncio.run(main(
        kernel=kernel,
        chat_service=llm,
        custom_function=custom_function,
        custom_plugin=custom_plugin
    ))
