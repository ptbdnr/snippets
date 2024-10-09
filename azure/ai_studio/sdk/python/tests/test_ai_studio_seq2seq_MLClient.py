import os
import pytest


def test_importable():
    import src.ai_studio_seq2seq_MLClient  # noqa: F401
    from src.ai_studio_seq2seq_MLClient import AIStudioSeq2SeqMLClient  # noqa: F401 E501


@pytest.fixture
def ai_studio_config() -> dict:
    """
    Load environment variables
    @return: dict with Open AI configuration
    """
    return {
        'tenant_id': os.getenv("AZURE_TENANT_ID"),
        'subscription_id': os.getenv("AZURE_SUBSCRIPTION_ID"),
        'resource_group_name': os.getenv("SEQ2SEQ_MLSTUDIO_RESOURCE_GROUP_NAME"),  # noqa E501
        'workspace_name': os.getenv("SEQ2SEQ_MLSTUDIO_WORKSPACE_NAME"),
        'endpoint_name': os.getenv("SEQ2SEQ_ENDPOINT_NAME"),
        'api_key': os.getenv("SEQ2SEQ_KEY"),
    }


def test_init():
    from src.ai_studio_seq2seq_MLClient import AIStudioSeq2SeqMLClient
    seq2seq = AIStudioSeq2SeqMLClient()
    assert seq2seq is not None


@pytest.mark.parametrize("messages", [
        [{'role': 'user', 'content': 'hi'}],
        [{'role': 'user', 'content': 'who are you?'}],
])
def test_chat(ai_studio_config, messages):
    from src.ai_studio_seq2seq_MLClient import AIStudioSeq2SeqMLClient
    seq2seq = AIStudioSeq2SeqMLClient(**ai_studio_config)
    response = seq2seq.chat(messages=messages)
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
