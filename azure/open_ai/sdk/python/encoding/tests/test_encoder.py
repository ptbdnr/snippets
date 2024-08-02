import pytest


def test_importable():
    import src.encoder  # noqa: F401
    from src.encoder import Encoder  # noqa: F401
    from src.encoder import EncoderProvider  # noqa: F401


class TestEncoder:

    from src.encoder import EncoderProvider

    def test_structure(self):
        from src.encoder import Encoder
        for method in ['new', 'encode']:
            assert hasattr(Encoder, method)
            assert callable(getattr(Encoder, method))

    @pytest.mark.parametrize("provider", [
        EncoderProvider.MOCKUP,
        EncoderProvider.OPENAI
    ])
    def test_new(self, provider):
        from src.encoder import Encoder
        encoder = Encoder.new(provider=provider)
        assert encoder is not None
