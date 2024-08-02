from abc import ABC, abstractmethod
from enum import Enum
from typing import List


class EncoderProvider(Enum):
    """
    Enum for embedding generator provider.
    """
    MOCKUP = "mockup"
    OPENAI = "openai"


class Encoder(ABC):
    """
    Abstract class for embedding generation.
    """

    @staticmethod
    def new(provider: EncoderProvider):
        match provider:
            case EncoderProvider.MOCKUP:
                from src.mockup_encoder import MockupEmbeddingGenerator
                return MockupEmbeddingGenerator()
            case EncoderProvider.OPENAI:
                from src.azure_openai_encoder import AzureOpenAIEncoder
                return AzureOpenAIEncoder()
            case _:
                raise ValueError(f"Invalid provider: {provider}")

    @abstractmethod
    def encode(self, text: str) -> List[float]:
        raise NotImplementedError
