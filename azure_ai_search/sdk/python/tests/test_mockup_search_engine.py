from collections.abc import Iterable

import pytest


def test_importable():
    import src.mockup_search_engine  # noqa: F401
    from src.mockup_search_engine import MockupSearchEngine  # noqa: F401


def test_init():
    from src.mockup_search_engine import MockupSearchEngine
    search_engine = MockupSearchEngine()
    assert search_engine is not None


@pytest.mark.parametrize("text", [
    ('foo'),
    ('bar')
])
def test_search(text):
    from src.mockup_search_engine import MockupSearchEngine
    search_engine = MockupSearchEngine()
    responses = search_engine.search(text=text)
    assert responses is not None
    assert isinstance(responses, Iterable)
    for response in responses:
        assert isinstance(response, dict)
