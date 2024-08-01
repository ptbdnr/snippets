import pytest


def test_importable():
    import src.storage  # noqa: F401
    from src.storage import StorageProvider  # noqa: F401
    from src.storage import Storage  # noqa: F401


class TestStorage:

    from src.storage import StorageProvider

    def test_structure(self):
        from src.storage import Storage
        for method in ['new', 'download_to_text']:
            assert hasattr(Storage, method)
            assert callable(getattr(Storage, method))

    @pytest.mark.parametrize("provider", [
        StorageProvider.MOCKUP,
        StorageProvider.AZURE_STORAGE_ACCOUNT,
    ])
    def test_new(self, provider):
        from src.storage import Storage
        storage = Storage.new(provider=provider)
        assert storage is not None
