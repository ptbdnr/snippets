import os
import logging
import json
import requests
from typing import List

from src.seq2seq import Seq2Seq
from src.encrypt import mask_key

# constants
ENV_KEY_SEQ2SEQ_ENDPOINT_URL = "SEQ2SEQ_ENDPOINT_URL"
ENV_KEY_SEQ2SEQ_KEY = "SEQ2SEQ_KEY"

class RequestsSeq2Seq(Seq2Seq):
    """
    Class to generate a text with requests
    """
    _endpoint_url: str
    _api_key: str

    def __init__(
        self,
        endpoint_url: str = None,
        api_key: str = None,
    ):
        logging.info("Start RequestsSeq2Seq configuration ...")

        self._endpoint_url = endpoint_url if endpoint_url \
            else os.getenv(ENV_KEY_SEQ2SEQ_ENDPOINT_URL)
        self._api_key = api_key if api_key \
            else os.getenv(ENV_KEY_SEQ2SEQ_KEY)

        # log configuration
        logging.info(f"Azure endpoint: {self._endpoint_url}")
        logging.info(f"Azure api_key: {mask_key(self._api_key, 2, -2)}")

        logging.info("Completed configuration.")
    
    def chat(self, messages: List[dict], **kwargs) -> str:
        """
        chat
        @param prompt: prompt text
        @return: chat text
        """
        logging.info("Start chat method ...")
        logging.info(f"kwargs: {json.dumps(kwargs)}")
        
        request_data = {
            "input_data": { "input_string": messages },  # seq2seq
            # "input_data": { "question": messages[-1]['content'], "context": 'dummy context'},  # qna
            # "messages": messages, 
            # **kwargs
            "parameters": {**kwargs}
        }

        # Remove this header to have the request observe
        # the endpoint traffic rules
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': ('Bearer ' + self._api_key)
        }

        try:
            response = requests.post(
                url=self._endpoint_url,
                headers=headers,
                data=str.encode(json.dumps(request_data))
            )

            # result = json.loads(response.text)[0]
            result = json.loads(response.text)['output']
            
            logging.info("Completed chatCompletion method.")
            return result
        
        except Exception as ex:
            logging.exception(f"{ex.code} {ex.info()} {ex.read().decode('utf8', 'ignore')}")
            raise ex
