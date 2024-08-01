import pytest


def test_importable():
    import src.search_engine  # noqa: F401
    from src.search_engine import SearchEngine  # noqa: F401
    from src.search_engine import SearchEngineProvider  # noqa: F401


class TestSearchEngine:

    from src.search_engine import SearchEngineProvider

    def test_structure(self):
        from src.search_engine import SearchEngine
        for method in ['new', 'search']:
            assert hasattr(SearchEngine, method)
            assert callable(getattr(SearchEngine, method))

    @pytest.mark.parametrize("provider", [
        SearchEngineProvider.MOCKUP,
        SearchEngineProvider.AZURE_AI_SEARCH,
    ])
    def test_new(self, provider):
        from src.search_engine import SearchEngine
        search_engine = SearchEngine.new(provider=provider)
        assert search_engine is not None

    @pytest.mark.xfail(reason='unkonw provider')
    @pytest.mark.parametrize("provider", [
        'foo'
    ])
    def test_new_fail(self, provider):
        from src.search_engine import SearchEngine
        search_engine = SearchEngine.new(provider=provider)
        assert search_engine is not None

    @pytest.mark.xfail(reason='abstract method')
    def test_search(self, provider):
        from src.search_engine import SearchEngine
        search_engine = SearchEngine.new(provider=provider)
        search_engine.search(text='foo')
