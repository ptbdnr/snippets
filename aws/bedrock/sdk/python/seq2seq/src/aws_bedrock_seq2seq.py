import os
import json
import logging
from typing import List

import boto3
from botocore.exceptions import ClientError

from src.seq2seq import Seq2Seq

ENV_KEY_REGION_NAME = os.getenv('SEQ2SEQ_BEDROCK_REGION')
ENV_KEY_BEDROCK_MODEL_ID = os.getenv('SEQ2SEQ_BEDROCK_MODEL_ID')


class AwsBedrockSeq2Seq(Seq2Seq):
    """
    Class to generate a text with AWS Bedrock
    """
    bedrock_client: boto3.client
    model_id: str

    def __init__(
            self,
            region: str = None,
            model_id: str = None,
            ):
        logging.info("Start AzureOpenAI client configuration ...")

        region = region if region \
            else os.getenv(ENV_KEY_REGION_NAME)
        model_id = model_id if model_id \
            else os.getenv(ENV_KEY_BEDROCK_MODEL_ID)

        # log configuration
        logging.info(f"AWS Bedrock region: {region}")
        logging.info(f"AWS Bedrock model_id: {model_id}")

        # construct LLM client
        self.bedrock_client = boto3.client(
            "bedrock-runtime",
            region_name=region
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

        conversation = []
        for msg in messages:
            conversation.append({
                'role': msg['role'],
                'content': [{'text': msg['content']}]
            })

        try:
            # Invoke the model with the request.
            responses = self.bedrock_client.converse(
                modelId=self.model_id,
                messages=conversation,
                inferenceConfig=kwargs
            )
        except (ClientError, Exception) as ex:
            print(f"ERROR: Can't invoke '{self.model_id}'. Reason: {ex}")
            exit(1)

        # select the first response
        response_text = responses["output"]["message"]["content"][0]["text"]

        logging.info("Completed chat method.")
        return response_text
