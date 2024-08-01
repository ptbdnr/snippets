import os

import pytest


def test_importable():
    import src.azure_storage_account  # noqa: F401
    from src.azure_storage_account import AzureStorageAccount  # noqa: F401


@pytest.fixture
def azure_ai_search_config() -> dict:
    return {
        "connection_string": os.getenv("STORAGE_AZURE_STORAGE_ACCOUNT_CONNECTION_STRING")
    }


class TestAzureStorageAccount:

    def test_init(self):
        from src.azure_storage_account import AzureStorageAccount
        storage = AzureStorageAccount()
        assert storage is not None

    @pytest.mark.parametrize("path, filename", [
        ('guidelines', 'JUST_Language_Guidelines_FINAL_14-10-21_(5) (1).json'),
    ])
    def test_download_to_text(self, azure_ai_search_config, path, filename):
        from src.azure_storage_account import AzureStorageAccount
        storage = AzureStorageAccount(**azure_ai_search_config)
        responses = storage.download_to_text(path=path, filename=filename)
        assert responses is not None
        assert isinstance(responses, str)
