from abc import ABC, abstractmethod
from enum import Enum
from typing import List


class Seq2SeqProvider(Enum):
    MOCKUP = 'mockup'
    AI_STUDIO = 'azure_ai_studio'
    REQUESTS = 'requests'


class Seq2Seq(ABC):
    """
    Abstract class for text generation
    """

    @staticmethod
    def new(provider: Seq2SeqProvider):
        match provider:
            case Seq2SeqProvider.MOCKUP:
                from src.mockup_seq2seq import MockupSeq2Seq
                return MockupSeq2Seq()
            case Seq2SeqProvider.AI_STUDIO:
                from src.ai_studio_seq2seq import AIStudioSeq2Seq
                return AIStudioSeq2Seq()
            case Seq2SeqProvider.REQUESTS:
                from src.requests_seq2seq import RequestsSeq2Seq
                return RequestsSeq2Seq()
            case _:
                raise ValueError(f"Invalid provider: {provider}")

    @abstractmethod
    def chat(self, messages: List[dict], **kwargs) -> str:
        raise NotImplementedError
