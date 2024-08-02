import pytest


def test_importable():
    import src.mockup_encoder  # noqa: F401
    from src.mockup_encoder import MockupEmbeddingGenerator  # noqa: F401


def test_init():
    from src.mockup_encoder import MockupEmbeddingGenerator
    embedding_generator = MockupEmbeddingGenerator()
    assert embedding_generator is not None


@pytest.mark.parametrize("text, str_startswith", [
    ("Hello, world!", "[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0")
])
def test_encode(text, str_startswith):
    from src.mockup_encoder import MockupEmbeddingGenerator
    embedding_generator = MockupEmbeddingGenerator()
    response = embedding_generator.encode(text)
    assert response is not None
    assert isinstance(response, list)
    assert str(response).startswith(str_startswith)
