import pytest


def test_importable():
    import src.aws_bedrock_seq2seq  # noqa: F401
    from src.aws_bedrock_seq2seq import AwsBedrockSeq2Seq  # noqa: F401


def test_init():
    from src.aws_bedrock_seq2seq import AwsBedrockSeq2Seq
    seq2seq = AwsBedrockSeq2Seq()
    assert seq2seq is not None


@pytest.mark.parametrize("messages", [
        [{'role': 'user', 'content': 'hi'}],
        [{'role': 'user', 'content': 'who are you?'}],
])
def test_chat(messages):
    from src.aws_bedrock_seq2seq import AwsBedrockSeq2Seq
    seq2seq = AwsBedrockSeq2Seq()
    response = seq2seq.chat(messages=messages)
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
