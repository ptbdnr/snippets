import os
from typing import Tuple

import pytest


def test_importable():
    import src.encoder  # noqa: F401
    from src.azure_openai_encoder import AzureOpenAIEncoder  # noqa: F401


@pytest.fixture
def openai_config() -> dict:
    """
    Load environment variables
    @return: dict with Open AI configuration
    """
    return {
        "azure_endpoint": os.getenv("ENCODER_OPENAI_ENDPOINT"),
        "api_key": os.getenv("ENCODER_OPENAI_KEY"),
        "api_version": os.getenv("ENCODER_OPENAI_API_VERSION"),
        "model": os.getenv("ENCODER_OPENAI_DEPLOYMENT_NAME"),
    }


def embedding_shape(model: str) -> Tuple[int, int]:
    """
    Get embedding shape
    @param model: model name
    @return: two-tuple of embedding shape \
        (Embedding Dimensions, Sequence Length))"""
    match model:
        case "text-embedding-ada-002":
            return (1536, 8191)
        case "text-embedding-3-small":
            return (1536, 8191)
        case "text-embedding-3-large":
            return (3072, 8191)
        case _:
            return (1536, 8191)


def test_init(openai_config):
    from src.azure_openai_encoder import AzureOpenAIEncoder
    encoder = AzureOpenAIEncoder(**openai_config)
    assert encoder is not None


@pytest.mark.parametrize("text, str_startswith", [
    ("Hello, world!", "[-0.019184619188308716, -0.025279032066464424,")
])
def test_encode(openai_config, text, str_startswith):
    from src.azure_openai_encoder import AzureOpenAIEncoder
    encoder = AzureOpenAIEncoder(**openai_config)
    response = encoder.encode(text)
    assert response is not None
    assert isinstance(response, list)
    assert len(response) == embedding_shape(encoder.model)[0]
    assert str(response).startswith(str_startswith)
