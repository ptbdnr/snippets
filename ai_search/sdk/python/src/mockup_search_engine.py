from collections.abc import Iterable

from src.search_engine import SearchEngine


class MockupSearchEngine(SearchEngine):
    """
    Mockup class for search.
    """

    def search(self, text: str) -> Iterable:
        """
        Search text
        @param text: search text
        @return: search results
        """

        record = {"foo": "bar"}
        return [record]
