from abc import ABC, abstractmethod
from enum import Enum
from typing import List


class Seq2SeqProvider(Enum):
    MOCKUP = 'mockup'
    AZURE_OPENAI = 'azure_openai'


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
            case Seq2SeqProvider.AZURE_OPENAI:
                from src.azure_openai_seq2seq import AzureOpenAISeq2Seq
                return AzureOpenAISeq2Seq()
            case _:
                raise ValueError(f"Invalid provider: {provider}")

    @abstractmethod
    def chat(self, messages: List[dict], **kwargs) -> str:
        raise NotImplementedError
