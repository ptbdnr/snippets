import os
import json
import logging
import urllib.request
import ssl
from typing import List

from src.seq2seq import Seq2Seq
from src.encrypt import mask_key


# constants
ENV_KEY_SEQ2SEQ_MLSTUDIO_ENDPOINT_URL = "SEQ2SEQ_ENDPOINT_URL"
ENV_KEY_SEQ2SEQ_MLSTUDIO_KEY = "SEQ2SEQ_KEY"


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


class RequestSeq2Seq(Seq2Seq):
    """
    Class to generate a mockup text
    """
    _endpoint_url: str
    _api_key: str
    
    def __init__(
        self,
        endpoint_url: str = None,
        api_key: str = None
    ):
        allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
        logging.info("Start RequestSeq2Seq configuration ...")

        self._endpoint_url = endpoint_url if endpoint_url \
            else os.getenv(ENV_KEY_SEQ2SEQ_MLSTUDIO_ENDPOINT_URL)
        self._api_key = api_key if api_key \
            else os.getenv(ENV_KEY_SEQ2SEQ_MLSTUDIO_KEY)

        # log configuration
        logging.info(f"Azure ML Studio endpoint: {self._endpoint_url}")
        logging.info(f"Azure ML Studio api_key: {mask_key(self._api_key, 2, -2)}")

        logging.info("Completed RequestSeq2Seq configuration.")


    def chat(self, messages: List[dict], **kwargs) -> str:
        """
        chat
        @param prompt: prompt text
        @return: chat text
        """
        logging.info("Start chat method ...")
        logging.info(f"kwargs: {json.dumps(kwargs)}")

        body = str.encode(json.dumps({
            # "input_data": { "input_string": messages }  # seq2seq
            "input_data": { "question": messages[-1]['content'], "context": 'dummy context'},  # qna
            # "messages": messages,
            **kwargs
        }))

        headers = {
            'Content-Type':'application/json', 
            'Authorization':('Bearer '+ self._api_key)
        }

        req = urllib.request.Request(
            url=self._endpoint_url, 
            data=body,
            headers=headers
        )

        try:
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf8', 'ignore')
            logging.info("Completed chatCompletion method.")
            logging.info(f"result: {result}")
            return result
        except urllib.error.HTTPError as error:
            logging.exception(f"{error.code} {error.info()} {error.read().decode('utf8', 'ignore')}")
            raise error
