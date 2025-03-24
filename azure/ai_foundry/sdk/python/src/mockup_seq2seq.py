from src.seq2seq import Seq2Seq
from typing import List


class MockupSeq2Seq(Seq2Seq):
    """
    Class to generate a mockup text
    """

    def chat(self, messages: List[dict], **kwargs) -> str:
        """
        mock
        @param messages: list of messages, each with keys 'role' and 'content'
        @return: completion
        """
        return 'mockup'
