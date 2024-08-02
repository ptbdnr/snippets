import os
import logging
import json
from typing import List

from openai import AzureOpenAI

from src.seq2seq import Seq2Seq
from src.encrypt import mask_key

# constants
ENV_KEY_SEQ2SEQ_OPENAI_ENDPOINT = "SEQ2SEQ_OPENAI_ENDPOINT"
ENV_KEY_SEQ2SEQ_OPENAI_KEY = "SEQ2SEQ_OPENAI_KEY"
ENV_KEY_SEQ2SEQ_OPENAI_DEPLOYMENT_NAME = "SEQ2SEQ_OPENAI_DEPLOYMENT_NAME"
ENV_KEY_SEQ2SEQ_OPENAI_API_VERSION = "SEQ2SEQ_OPENAI_API_VERSION"


class AzureOpenAISeq2Seq(Seq2Seq):
    """
    Class to generate a text with Azure OpenAI
    """
    openai_client: AzureOpenAI
    model: str

    def __init__(
            self,
            azure_endpoint: str = None,
            api_key: str = None,
            api_version: str = None,
            model: str = None,
            ):
        logging.info("Start AzureOpenAI client configuration ...")

        azure_endpoint = azure_endpoint if azure_endpoint \
            else os.getenv(ENV_KEY_SEQ2SEQ_OPENAI_ENDPOINT)
        api_key = api_key if api_key \
            else os.getenv(ENV_KEY_SEQ2SEQ_OPENAI_KEY)
        api_version = api_version if api_version \
            else os.getenv(ENV_KEY_SEQ2SEQ_OPENAI_API_VERSION)
        self.model = model if model \
            else os.getenv(ENV_KEY_SEQ2SEQ_OPENAI_DEPLOYMENT_NAME)

        # log configuration
        logging.info(f"Azure OpenAI azure_endpoint: {azure_endpoint}")
        logging.info(f"Azure OpenAI api_key: {mask_key(api_key, 2, -2)}")
        logging.info(f"Azure OpenAI api_version: {api_version}")
        logging.info(f"Azure OpenAI model: {self.model}")

        # construct LLM client
        self.openai_client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version=api_version,
        )

        logging.info("Completed AzureOpenAI client configuration.")

    def chat(self, messages: List[dict], **kwargs) -> str:
        """
        chat
        @param prompt: prompt text
        @return: chat text
        """
        logging.info("Start chat method ...")
        logging.info(f"kwargs: {json.dumps(kwargs)}")

        try:
            responses = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs,
            )
        except Exception as ex:
            msg = f"Error({type(ex).__name}) in chat: {str(ex)}"
            logging.exception(msg)

        logging.info("responses: " + str(responses))

        # select the first response
        response = responses.choices[0].message.content

        logging.info("Completed chat method.")

        return response
