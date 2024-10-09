# References:
# * https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script  # noqa E501
import os
import logging
import json
import requests
from typing import List

from azure.ai.ml import MLClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import InteractiveBrowserCredential
# from azure.identity import DefaultAzureCredential

from src.seq2seq import Seq2Seq
from src.encrypt import mask_key

# constants
ENV_KEY_AZURE_TENANT_ID = "AZURE_TENANT_ID"
ENV_KEY_AZURE_SUBSCRIPTION_ID = "AZURE_SUBSCRIPTION_ID"
ENV_KEY_SEQ2SEQ_MLSTUDIO_RESOURCE_GROUP_NAME = "SEQ2SEQ_MLSTUDIO_RESOURCE_GROUP_NAME"  # noqa E501
ENV_KEY_SEQ2SEQ_MLSTUDIO_WORKSPACE_NAME = "SEQ2SEQ_MLSTUDIO_WORKSPACE_NAME"
ENV_KEY_SEQ2SEQ_ENDPOINT_NAME = "SEQ2SEQ_ENDPOINT_NAME"
ENV_KEY_SEQ2SEQ_KEY = "SEQ2SEQ_KEY"



class AIStudioSeq2SeqMLClient(Seq2Seq):
    """
    Class to generate a text with Azure AI Studio
    """
    ml_client: MLClient
    _endpoint_name: str
    _api_key: str

    def __init__(
        self,
        tenant_id: str = None,
        subscription_id: str = None,
        resource_group_name: str = None,
        workspace_name: str = None,
        endpoint_name: str = None,
        api_key: str = None,
    ):
        logging.info("Start AI Studio configuration ...")

        self._tenant_id = tenant_id if tenant_id \
            else os.getenv(ENV_KEY_AZURE_TENANT_ID)
        self._subscription_id = subscription_id if subscription_id \
            else os.getenv(ENV_KEY_AZURE_SUBSCRIPTION_ID)
        self._resource_group_name = resource_group_name if resource_group_name \
            else os.getenv(ENV_KEY_SEQ2SEQ_MLSTUDIO_RESOURCE_GROUP_NAME)
        self._workspace_name = workspace_name if workspace_name \
            else os.getenv(ENV_KEY_SEQ2SEQ_MLSTUDIO_WORKSPACE_NAME)
        self._endpoint_name = endpoint_name if endpoint_name \
            else os.getenv(ENV_KEY_SEQ2SEQ_ENDPOINT_NAME)
        self._api_key = api_key if api_key \
            else os.getenv(ENV_KEY_SEQ2SEQ_KEY)

        # log configuration
        logging.info(f"Azure tenant_id: {self._tenant_id}")
        logging.info(f"Azure subscription_id: {self._subscription_id}")
        logging.info(f"Azure ML Studio resource_group: {self._resource_group_name}")
        logging.info(f"Azure ML Studio workspace_name: {self._workspace_name}")
        logging.info(f"Azure endpoint: {self._endpoint_name}")
        logging.info(f"Azure api_key: {mask_key(self._api_key, 2, -2)}")

        logging.info("Completed AI Studio configuration.")

    def _init_ml_client(self) -> None:
        credential = InteractiveBrowserCredential(tenant_id=self._tenant_id)
        
        self.ml_client = MLClient(
            credential=credential,
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name,
        )
    
    def chat(self, messages: List[dict], **kwargs) -> str:
        """
        chat
        @param prompt: prompt text
        @return: chat text
        """
        logging.info("Start chat method ...")
        logging.info(f"kwargs: {json.dumps(kwargs)}")
        
        request_data = {
            "input_data": { "input_string": messages }, # seq2seq
            # "messages": messages 
            # "input_data": { "question": messages[-1]['content'], "context": 'dummy context'} # qna
            **kwargs
        }

        # Remove this header to have the request observe
        # the endpoint traffic rules
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': ('Bearer ' + self._api_key)
        }

        self._init_ml_client()
        endpoint_url = self.ml_client.online_endpoints.get(self._endpoint_name).scoring_uri

        response = requests.post(
            url=endpoint_url,
            headers=headers,
            data=str.encode(json.dumps(request_data))
        )

        result = json.loads(response.text)['output']

        logging.info("Completed chatCompletion method.")
        logging.info(f"result: {result}")

        return result
