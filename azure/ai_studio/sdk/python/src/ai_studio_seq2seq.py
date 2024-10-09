# References:
# * https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script  # noqa E501
import os
import logging
import json
# import urllib.request
# import ssl
from typing import List

from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

from src.seq2seq import Seq2Seq
from src.encrypt import mask_key

# constants
ENV_KEY_SEQ2SEQ_ENDPOINT_URL = "SEQ2SEQ_ENDPOINT_URL"
ENV_KEY_SEQ2SEQ_KEY = "SEQ2SEQ_KEY"


class AIStudioSeq2Seq(Seq2Seq):
    """
    Class to generate a text with Azure AI Studio
    """
    _chat_client: ChatCompletionsClient
    _endpoint_url: str
    _api_key: str

    def __init__(
        self,
        endpoint_url: str = None,
        api_key: str = None,
    ):
        logging.info("Start AI Studio configuration ...")

        self._endpoint_url = endpoint_url if endpoint_url \
            else os.getenv(ENV_KEY_SEQ2SEQ_ENDPOINT_URL)
        self._api_key = api_key if api_key \
            else os.getenv(ENV_KEY_SEQ2SEQ_KEY)

        # log configuration
        logging.info(f"Azure AI Studio azure_endpoint: {self._endpoint_url}")
        logging.info(f"Azure AI Studio api_key: {mask_key(self._api_key, 2, -2)}")

        logging.info("Completed AI Studio configuration.")

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

        result = response.choices[0].message.content
        logging.info("Completed chatCompletion method.")

        return result
