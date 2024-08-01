from abc import ABC, abstractmethod
from enum import Enum
from collections.abc import Iterable


class SearchEngineProvider(Enum):
    MOCKUP = "mockup"
    AZURE_AI_SEARCH = "azure_ai_search"


class SearchEngine(ABC):
    """
    Abstract class for search engine
    """

    @staticmethod
    def new(provider: SearchEngineProvider):
        match provider:
            case SearchEngineProvider.MOCKUP:
                from src.mockup_search_engine import MockupSearchEngine
                return MockupSearchEngine()
            case SearchEngineProvider.AZURE_AI_SEARCH:
                from src.azure_ai_search_engine import AzureAISearchEngine
                return AzureAISearchEngine()
            case _:
                raise ValueError(f"Invalid provider: {provider}")

    @abstractmethod
    def search(self, text: str) -> Iterable:
        raise NotImplementedError
