import os
import json
import requests

import dotenv

dotenv.load_dotenv('env')

OPENAI_API_CHAT_ENDPOINT_URL = os.getenv('SEQ2SEQ_ENDPOINT_URL')
OPENAI_API_CHAT_KEY = os.getenv('SEQ2SEQ_KEY')

print(OPENAI_API_CHAT_ENDPOINT_URL)

messages = [{'role': 'user', 'content': 'Who are you? Be concise.'}]

request_data = {
    "messages": messages,
    "temperature": 0.2,
    "top_p": 0.5,
    "max_tokens": 125,
    "presence_penalty": 0,
    "frequency_penalty": 0
}

headers = {
    'Authorization':('Bearer '+ OPENAI_API_CHAT_KEY),
    'Content-Type':'application/json', 
    'Accept': 'application/json'
}

response = requests.post(
    url=OPENAI_API_CHAT_ENDPOINT_URL + '/v1/chat/completions', # expected: OpenAI chat API interface for respose object
    headers=headers,
    data=str.encode(json.dumps(request_data))
)

print(json.dumps(json.loads(response.text), indent=2))