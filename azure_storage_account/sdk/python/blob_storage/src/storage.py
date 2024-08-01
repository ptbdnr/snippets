from abc import ABC
from enum import Enum


class StorageProvider(Enum):
    MOCKUP = "mockup"
    AZURE_STORAGE_ACCOUNT = "azure_storage_account"


class Storage(ABC):
    """
    Abstract class for storage
    """

    @staticmethod
    def new(provider: StorageProvider):
        match provider:
            case StorageProvider.MOCKUP:
                from src.mockup_storage import MockupStorage
                return MockupStorage()
            case StorageProvider.AZURE_STORAGE_ACCOUNT:
                from src.azure_storage_account import AzureStorageAccount
                return AzureStorageAccount()
            case _:
                raise ValueError(f"Invalid provider: {provider}")

    @classmethod
    def download_to_text(self, path: str, filename: str) -> str:
        raise NotImplementedError
