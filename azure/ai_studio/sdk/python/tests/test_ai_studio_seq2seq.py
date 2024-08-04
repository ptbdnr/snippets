import os
import pytest


def test_importable():
    import src.ai_studio_seq2seq  # noqa: F401
    from src.ai_studio_seq2seq import AIStudioSeq2Seq  # noqa: F401


@pytest.fixture
def ai_studio_config() -> dict:
    """
    Load environment variables
    @return: dict with Open AI configuration
    """
    return {
        "azure_endpoint": os.getenv("SEQ2SEQ_AISTUDIO_ENDPOINT"),
        "api_key": os.getenv("SEQ2SEQ_AISTUDIO_KEY"),
    }


def test_init():
    from src.ai_studio_seq2seq import AIStudioSeq2Seq
    seq2seq = AIStudioSeq2Seq()
    assert seq2seq is not None


@pytest.mark.parametrize("messages", [
        [{'role': 'user', 'content': 'hi'}],
        [{'role': 'user', 'content': 'who are you?'}],
])
def test_chat(ai_studio_config, messages):
    from src.ai_studio_seq2seq import AIStudioSeq2Seq
    seq2seq = AIStudioSeq2Seq(**ai_studio_config)
    response = seq2seq.chat(messages=messages)
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
