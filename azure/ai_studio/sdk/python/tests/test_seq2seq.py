import pytest


def test_importable():
    import src.seq2seq  # noqa: F401
    from src.seq2seq import Seq2Seq  # noqa: F401
    from src.seq2seq import Seq2SeqProvider  # noqa: F401


class TestSeq2Seq:

    from src.seq2seq import Seq2SeqProvider

    def test_structure(self):
        from src.seq2seq import Seq2Seq
        for method in ['new', 'chat']:
            assert hasattr(Seq2Seq, method)
            assert callable(getattr(Seq2Seq, method))

    @pytest.mark.parametrize("provider", [
        Seq2SeqProvider.MOCKUP,
        Seq2SeqProvider.AI_STUDIO
    ])
    def test_new(self, provider):
        from src.seq2seq import Seq2Seq
        seq2seq = Seq2Seq.new(provider=provider)
        assert seq2seq is not None

    @pytest.mark.xfail(reason='unkonw provider')
    @pytest.mark.parametrize("provider", [
        'foo'
    ])
    def test_new_fail(self, provider):
        from src.seq2seq import Seq2Seq
        seq2seq = Seq2Seq.new(provider=provider)
        assert seq2seq is not None

    @pytest.mark.xfail(reason='abstract method')
    def test_chat(self, provider):
        from src.seq2seq import Seq2Seq
        seq2seq = Seq2Seq.new(provider=provider)
        seq2seq.chat(messages=None)
