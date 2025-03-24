import os
import pytest


def test_importable():
    import src.requests_seq2seq  # noqa: F401
    from src.requests_seq2seq import RequestsSeq2Seq  # noqa: F401 E501


@pytest.fixture
def ai_studio_config() -> dict:
    """
    Load environment variables
    @return: dict with Open AI configuration
    """
    return {
        'endpoint_url': os.getenv("SEQ2SEQ_ENDPOINT_URL"),
        'api_key': os.getenv("SEQ2SEQ_KEY"),
    }


def test_init():
    from src.requests_seq2seq import RequestsSeq2Seq
    seq2seq = RequestsSeq2Seq()
    assert seq2seq is not None


@pytest.mark.parametrize("messages", [
        [{'role': 'user', 'content': 'hi'}],
        [{'role': 'user', 'content': 'who are you?'}],
])
def test_chat(ai_studio_config, messages):
    from src.requests_seq2seq import RequestsSeq2Seq
    seq2seq = RequestsSeq2Seq(**ai_studio_config)
    response = seq2seq.chat(messages=messages)
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
