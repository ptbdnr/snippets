import os
import pytest


def test_importable():
    import src.request_seq2seq  # noqa: F401
    from src.request_seq2seq import RequestSeq2Seq  # noqa: F401


@pytest.fixture
def request_config() -> dict:
    """
    Load environment variables
    @return: dict with Open AI configuration
    """
    return {
        "endpoint_url": os.getenv("SEQ2SEQ_ENDPOINT_URL"),
        "api_key": os.getenv("SEQ2SEQ_KEY"),
    }


def test_init():
    from src.request_seq2seq import RequestSeq2Seq
    seq2seq = RequestSeq2Seq()
    assert seq2seq is not None


@pytest.mark.parametrize("messages", [
        [{'role': 'user', 'content': 'hi'}],
        [{'role': 'user', 'content': 'who are you?'}],
])
def test_chat(request_config, messages):
    from src.request_seq2seq import RequestSeq2Seq
    seq2seq = RequestSeq2Seq(**request_config)
    response = seq2seq.chat(messages=messages)
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
