# G-Eval
# credit to https://github.com/nlpyang/geval/tree/main

import os

import dotenv

from openai import AzureOpenAI

dotenv.load_dotenv('env')

prompt_tempate = """
You will be given one summary written for a news article.
Your task is to rate the summary on one metric.
Please make sure you read and understand these instructions carefully. Please keep this document open while reviewing, and refer to it as needed.

Evaluation Criteria:
Coherence (1-5) - the collective quality of all sentences. We align this dimension with the DUC quality question of structure and coherence whereby "the summary should be well-structured and well-organized. The summary should not just be a heap of related information, but should build from sentence to a coherent body of information about a topic."

Evaluation Steps:
1. Read the news article carefully and identify the main topic and key points.
2. Read the summary and compare it to the news article. Check if the summary covers the main topic and key points of the news article, and if it presents them in a clear and logical order.
3. Assign a score for coherence on a scale of 1 to 5, where 1 is the lowest and 5 is the highest based on the Evaluation Criteria.

Source Text:
{Document}

Summary:
{Summary}


Evaluation Form (scores ONLY):

- Coherence:
"""

messages = [{
    'role': 'user', 
    'content': prompt_tempate.format_map({
        'Document': "A transformer is a deep learning architecture developed by researchers at Google and based on the multi-head attention mechanism, proposed in the 2017 paper \"Attention Is All You Need\".[1] Text is converted to numerical representations called tokens, and each token is converted into a vector via lookup from a word embedding table.[1] At each layer, each token is then contextualized within the scope of the context window with other (unmasked) tokens via a parallel multi-head attention mechanism, allowing the signal for key tokens to be amplified and less important tokens to be diminished. Transformers have the advantage of having no recurrent units, therefore requiring less training time than earlier recurrent neural architectures (RNNs) such as long short-term memory (LSTM).[2] Later variations have been widely adopted for training large language models (LLM) on large (language) datasets, such as the Wikipedia corpus and Common Crawl.[3] Transformers were first developed as an improvement over previous architectures for machine translation,[4][5] but have found many applications since. They are used in large-scale natural language processing, computer vision (vision transformers), reinforcement learning,[6][7] audio,[8] multimodal learning, robotics,[9] and even playing chess.[10] It has also led to the development of pre-trained systems, such as generative pre-trained transformers (GPTs)[11] and BERT[12] (bidirectional encoder representations from transformers).",
        'Summary': "A transformer is a deep learning architecture pattern."
    })
}]

openai_client = AzureOpenAI(
    azure_endpoint=os.getenv('OPENAI_CHAT_ENDPOINT_URL'),
    api_key=os.getenv('OPENAI_CHAT_ENDPOINT_KEY'),
    api_version=os.getenv('OPENAI_CHAT_ENDPOINT_API_VERSION')I_CHAT_ENDPOINT_API_VERSION,
)

try:
    response = openai_client.chat.completions.create(
        model=os.getenv('OPENAI_CHAT_ENDPOINT_DEPLOYMENT_NAME'),
        messages=messages
    )

    print(f"id: {response.id}")
    print(f"created: {response.created}")
    print(f"model: {response.model}")
    print("choices:")
    for choice in response.choices:
        print(f" choice: {choice.index}")
        print(f" message.role: {choice.message.role}")
        print(f" message.content: {choice.message.content}")
except Exception as ex:
    print(f"Error({type(ex).__name}) in chat: {str(ex)}")