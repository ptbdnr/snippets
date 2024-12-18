import os
import asyncio
from datetime import datetime, timedelta

import dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import (
    kernel_function,
    KernelArguments
)
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior
)


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


print('=' * 16 + '\n' + 'TOOL OUTPUT (2 day ahead)')
print(DatetimeLookAheadPlugin().x_days_ahead(offset=2))

print('=' * 16 + '\n' + 'TOOL OUTPUT (2 hours ahead)')
print(DatetimeLookAheadPlugin().x_hours_ahead(offset=2))


async def main(
    kernel: Kernel,
    chat_service: AzureChatCompletion
):
    # Enable automatic function calling
    prompt_execution_settings = kernel.\
        get_prompt_execution_settings_from_service_id(
            service_id=chat_service.service_id
        )
    prompt_execution_settings.function_choice_behavior = \
        FunctionChoiceBehavior.Auto(auto_invoke=True)
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
        chat_service=llm
    ))
