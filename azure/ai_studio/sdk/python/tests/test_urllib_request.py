import os
import pytest


def test_importable():
    import src.urllib_request  # noqa: F401
    from src.urllib_request import UrllibRequest  # noqa: F401


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
    from src.urllib_request import UrllibRequest
    requestHandler = UrllibRequest()
    assert requestHandler is not None


@pytest.mark.parametrize("messages", [
        [{'role': 'user', 'content': 'hi'}],
        [{'role': 'user', 'content': 'who are you?'}],
])
def test_chat(request_config, messages):
    from src.urllib_request import UrllibRequest
    requestHandler = UrllibRequest(**request_config)
    response = requestHandler.chat(messages=messages)
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.parametrize("input_data", [
        ["This is a simple example."],
        ["Wow! Awesome test.", "Boo! Rubbish test."],
])
def test_text_classification(request_config, input_data):
    from src.urllib_request import UrllibRequest
    requestHandler = UrllibRequest(**request_config)
    response = requestHandler.text_classification(input_data=input_data)
    assert response is not None
    assert isinstance(response, list)
    assert len(response) > 0
