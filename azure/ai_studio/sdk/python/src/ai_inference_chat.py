# Ref.: https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script  # noqa E501
import os
import logging
import json

from typing import List

from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

from src.encrypt import mask_key


# constants
ENV_KEY_SEQ2SEQ_ENDPOINT_URL = "SEQ2SEQ_ENDPOINT_URL"
ENV_KEY_SEQ2SEQ_KEY = "SEQ2SEQ_KEY"


class AIInferenceChat:
    """
    Class to generate a text with Azure AI Inference ChatCompletionsClient
    """
    _chat_client: ChatCompletionsClient
    _endpoint_url: str
    _api_key: str

    def __init__(
        self,
        endpoint_url: str = None,
        api_key: str = None,
    ):
        logging.info("Start AI Inference ChatCompletionsClient configuration ...")

        self._endpoint_url = endpoint_url if endpoint_url \
            else os.getenv(ENV_KEY_SEQ2SEQ_ENDPOINT_URL)
        self._api_key = api_key if api_key \
            else os.getenv(ENV_KEY_SEQ2SEQ_KEY)

        # log configuration
        logging.info(f"Azure AI Studio endpoint_ulr: {self._endpoint_url}")
        logging.info(f"Azure AI Studio api_key: {mask_key(self._api_key, 2, -2)}")

        logging.info("Completed AI Inference ChatCompletionsClient configuration.")

    def _init_chat_client(self) -> None:
        credential = AzureKeyCredential(self._api_key)
        self._chat_client = ChatCompletionsClient(
            endpoint=self._endpoint_url,
            credential=credential
        )

    def chat(self, messages: List[dict], **kwargs) -> str:
        """
        chat
        @param prompt: prompt text
        @return: chat text
        """
        logging.info("Start chat method ...")
        logging.info(f"kwargs: {json.dumps(kwargs)}")

        self._init_chat_client()

        response = self._chat_client.complete(
            messages=messages,
            model_extras=kwargs
        )

        # OpenAI chat API interface for respose object
        print(f"id: {response.id}")
        print(f"created: {response.created}")
        print(f"model: {response.model}")
        print(f"usage: {response.usage}")
        print("choices:")
        for choice in response.choices:
            print(f" choice: {choice.index}")
            print(f" finish_reason: {choice.finish_reason}")
            print(f" message.role: {choice.message.role}")
            print(f" message.content: {choice.message.content}")
            print(f" message.tool_calls: {choice.message.tool_calls}")

        logging.info("Completed chatCompletion method.")

        return response.choices[0].message.content
