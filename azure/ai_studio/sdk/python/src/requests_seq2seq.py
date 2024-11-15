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
        @param messages: list of messages, with format [{'role': 'user', 'content': 'foo'}]
        @return: response text
        """
        logging.info("Start chat method ...")
        logging.info(f"kwargs: {json.dumps(kwargs)}")
        
        request_data = { 
            "messages": messages, 
            **kwargs
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
                url=self._endpoint_url, # + 'v1/chat/completions'
                headers=headers,
                data=str.encode(json.dumps(request_data))
            )

            result = json.loads(response.text)
            
            logging.info("Completed chatCompletion method.")
            return result
        
        except Exception as ex:
            logging.exception(f"{ex.code} {ex.info()} {ex.read().decode('utf8', 'ignore')}")
            raise ex


    def completion(self, input_strings: List[str], **kwargs) -> str:
        """
        completion
        @param input_strings: list of input prompts
        @return: completion text
        """
        logging.info("Start chat method ...")
        logging.info(f"kwargs: {json.dumps(kwargs)}")
        
        request_data = { 
            "input_data": { "input_string": input_strings },
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
                url=self._endpoint_url, # + '/score'
                headers=headers,
                data=str.encode(json.dumps(request_data))
            )

            result = json.loads(response.text)[0]
            
            logging.info("Completed chatCompletion method.")
            return result
        
        except Exception as ex:
            logging.exception(f"{ex.code} {ex.info()} {ex.read().decode('utf8', 'ignore')}")
            raise ex
    

    def q_and_a(self, question: str, context: str = None, **kwargs) -> str:
        """
        q_and_a
        @param question: question text
        @param context: context text
        @return: answer text
        """
        logging.info("Start chat method ...")
        logging.info(f"kwargs: {json.dumps(kwargs)}")
        
        request_data = {
            "input_data": { "question": question, "context": context},
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
                url=self._endpoint_url,  # + '/score'
                headers=headers,
                data=str.encode(json.dumps(request_data))
            )

            result = json.loads(response.text)['output']
            
            logging.info("Completed chatCompletion method.")
            return result
        
        except Exception as ex:
            logging.exception(f"{ex.code} {ex.info()} {ex.read().decode('utf8', 'ignore')}")
            raise ex
