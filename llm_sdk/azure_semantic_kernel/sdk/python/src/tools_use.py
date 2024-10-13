import os
import asyncio
from datetime import datetime, timedelta

import dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import (
    kernel_function,
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


class DatetimeLookAheadPlugin:
    @kernel_function(
        name='XDaysAhead',
        description="Return the date x days ahead."
    )
    def x_days_ahead(self, offset: int) -> str:
        new_date = datetime.now() + timedelta(days=offset)
        return new_date.strftime("%Y-%m-%d")

    @kernel_function(
        name='XHoursAhead',
        description="Return the time x hours ahead."
    )
    def x_hours_ahead(self, offset: int) -> str:
        """Return the time x hours ahead."""
        new_date = datetime.now() + timedelta(hours=offset)
        return new_date.strftime("%H:%M:%S")


custom_plugin = kernel.add_plugin(
    plugin=DatetimeLookAheadPlugin(),
    plugin_name="DatetimeLookAhead"
)


async def main(
    kernel: Kernel,
    chat_service: AzureChatCompletion,
    custom_plugin: KernelPlugin
) -> None:
    pass

    result = await custom_plugin.get('XDaysAhead').invoke(
        kernel=kernel,
        offset=2
    )
    print('=' * 16 + '\n' + 'PLUGIN OUTPUT (2 day ahead)')
    print(result)

    result = await custom_plugin.get('XHoursAhead').invoke(
        kernel=kernel,
        offset=2
    )
    print('=' * 16 + '\n' + 'PLUGIN OUTPUT (2 hours ahead)')
    print(result)

    # Invoke the model
    prompt_execution_settings = kernel.\
        get_prompt_execution_settings_from_service_id(
            service_id=chat_service.service_id
        )

    messages = ChatHistory()
    messages.add_system_message("What is the date in 2 days?"),
    result = await chat_service.get_chat_message_content(
        chat_history=messages,
        kernel=kernel,
        settings=prompt_execution_settings
    )
    print('=' * 16 + '\n' + 'MODEL OUTPUT WITHOUT TOOL')
    print(result)

    messages = ChatHistory()
    messages.add_system_message("What is the time in 2 hours?"),
    result = await chat_service.get_chat_message_content(
        chat_history=messages,
        kernel=kernel,
        settings=prompt_execution_settings
    )
    print('=' * 16 + '\n' + 'MODEL OUTPUT WITHOUT TOOL')
    print(result)

    # Allow tool to the model
    prompt_execution_settings.function_choice_behavior = \
        FunctionChoiceBehavior.Auto()
    messages = ChatHistory()
    messages.add_system_message("What is the datetime in 2 days and 2 hours?"),
    result = await chat_service.get_chat_message_contents(
        chat_history=messages,
        settings=prompt_execution_settings,
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
        custom_plugin=custom_plugin
    ))
