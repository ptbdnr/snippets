import pytest


def test_importable():
    import src.mockup_storage  # noqa: F401
    from src.mockup_storage import MockupStorage  # noqa: F401


def test_init():
    from src.mockup_storage import MockupStorage
    storage = MockupStorage()
    assert storage is not None


@pytest.mark.parametrize("path, filename", [
    ('foo', '1'),
    ('bar', '2')
])
def test_download_to_text(path, filename):
    from src.mockup_storage import MockupStorage
    storage = MockupStorage()
    responses = storage.download_to_text(path=path, filename=filename)
    assert responses is not None
    assert isinstance(responses, str)
