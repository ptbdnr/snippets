import pytest


def test_importable():
    import src.mockup_seq2seq  # noqa: F401
    from src.mockup_seq2seq import MockupSeq2Seq  # noqa: F401


def test_init():
    from src.mockup_seq2seq import MockupSeq2Seq
    seq2seq = MockupSeq2Seq()
    assert seq2seq is not None


@pytest.mark.parametrize("messages", [
        [{'role': 'user', 'content': 'hi'}],
        [{'role': 'user', 'content': 'who are you?'}],
])
def test_chat(messages):
    from src.mockup_seq2seq import MockupSeq2Seq
    seq2seq = MockupSeq2Seq()
    response = seq2seq.chat(messages=messages)
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
