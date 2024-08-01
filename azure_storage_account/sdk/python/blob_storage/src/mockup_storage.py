import json

from src.storage import Storage


class MockupStorage(Storage):
    """
    Mockup class for storage.
    """

    def download_to_text(self, path: str, filename: str) -> str:
        """
        Return data in text
        @param path: path to file
        @filename: filename
        @return: text
        """

        data = {"foo": "bar"}
        return json.dumps(data)
