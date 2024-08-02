import os
import logging
from typing import List

from openai import AzureOpenAI

from src.encoder import Encoder
from src.encrypt import mask_key

# constants
ENV_KEY_ENCODER_OPENAI_ENDPOINT = "ENCODER_OPENAI_ENDPOINT"
ENV_KEY_ENCODER_OPENAI_KEY = "ENCODER_OPENAI_KEY"
ENV_KEY_ENCODER_OPENAI_DEPLOYMENT_NAME = "ENCODER_OPENAI_DEPLOYMENT_NAME"
ENV_KEY_ENCODER_OPENAI_API_VERSION = "ENCODER_OPENAI_API_VERSION"


class AzureOpenAIEncoder(Encoder):
    """
    Class for generate embeddings
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
            else os.getenv(ENV_KEY_ENCODER_OPENAI_ENDPOINT)
        api_key = api_key if api_key \
            else os.getenv(ENV_KEY_ENCODER_OPENAI_KEY)
        api_version = api_version if api_version \
            else os.getenv(ENV_KEY_ENCODER_OPENAI_API_VERSION)
        self.model = model if model \
            else os.getenv(ENV_KEY_ENCODER_OPENAI_DEPLOYMENT_NAME)

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

    def encode(self, text: str) -> List[float]:
        """
        Generate embeddings
        @param text: text to generate embeddings
        @return: embeddings
        """
        logging.info("Start encode method ...")

        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model=self.model
            )
        except Exception as ex:
            msg = f"Error({type(ex).__name}) in embeddings: {str(ex)}"
            logging.exception(msg)

        # select first embedding
        embeddings = response.model_dump()['data'][0]['embedding']
        
        logging.info("Completed encode method.")
        return embeddings
