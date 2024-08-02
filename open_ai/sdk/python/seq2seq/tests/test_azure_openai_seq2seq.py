import os
import pytest


def test_importable():
    import src.azure_openai_seq2seq  # noqa: F401
    from src.azure_openai_seq2seq import AzureOpenAISeq2Seq  # noqa: F401


@pytest.fixture
def openai_config() -> dict:
    return {
        "azure_endpoint": os.getenv("SEQ2SEQ_OPENAI_ENDPOINT"),
        "api_key": os.getenv("SEQ2SEQ_OPENAI_KEY"),
        "api_version": os.getenv("SEQ2SEQ_OPENAI_API_VERSION"),
        "model": os.getenv("SEQ2SEQ_OPENAI_DEPLOYMENT_NAME"),
    }


def test_init(openai_config):
    from src.azure_openai_seq2seq import AzureOpenAISeq2Seq
    seq2seq = AzureOpenAISeq2Seq(**openai_config)
    assert seq2seq is not None


@pytest.mark.parametrize("messages", [
        [{'role': 'user', 'content': 'hi'}],
        [{'role': 'user', 'content': 'who are you?'}],
])
def test_chat(openai_config, messages):
    from src.azure_openai_seq2seq import AzureOpenAISeq2Seq
    seq2seq = AzureOpenAISeq2Seq(**openai_config)
    response = seq2seq.chat(messages=messages)
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
