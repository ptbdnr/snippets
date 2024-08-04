# ref:
# * https://learn.microsoft.com/en-us/azure/search/search-lucene-query-architecture
# * https://docs.microsoft.com/en-us/azure/search/query-lucene-syntax#bkmk_ranking
# * https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview

import os
import logging
from collections.abc import Iterable
from typing import List, Dict
from enum import Enum

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, CorsOptions, ScoringProfile,
    SimpleField, ComplexField, SearchableField, SearchField,
    SearchFieldDataType,
    VectorSearch, HnswAlgorithmConfiguration, VectorSearchProfile
)

from src.search_engine import SearchEngine
from src.encrypt import mask_key

# constants
ENV_KEY_SEARCH_ENGINE_AISEARCH_ENDPOINT = os.getenv(
    'SEARCH_ENGINE_AISEARCH_ENDPOINT')
ENV_KEY_SEARCH_ENGINE_AISEARCH_KEY = os.getenv(
    'SEARCH_ENGINE_AISEARCH_KEY')
ENV_KEY_SEARCH_ENGINE_AISEARCH_INDEX_NAME = os.getenv(
    'SEARCH_ENGINE_AISEARCH_INDEX_NAME')

FIELD_TYPE_MAPPING = {
    'simple': SimpleField,
    'complex': ComplexField,
    'searchable': SearchableField,
    'search': SearchField,
}
SEARCH_FIELD_DATA_TYPE_MAPPING = {
    'string': SearchFieldDataType.String,
    'double': SearchFieldDataType.Double,
    'vector': SearchFieldDataType.Collection(SearchFieldDataType.Single),
}

NUMBER_OF_NEIGHBORS = 999  # number of neighbors to return
NUMBER_OF_NEIGHBORS_FOR_TEXT_SEARCH = NUMBER_OF_NEIGHBORS
NUMBER_OF_NEIGHBORS_FOR_VECTOR_SEARCH = NUMBER_OF_NEIGHBORS
DEFAULT_SEMANTIC_SCORE_VALUE = 0.0  # to avoid NoneType error
SEARCH_FIELDS = ['content_text']
VECTOR_FIELDS = 'content_vector'
QUERY_LANGUAGE = 'en-us'
SELECT_FIELDS = ['foo', 'bar', 'buz']


class TextSearchType(Enum):
    SIMPLE = 'simple'
    FULL = 'full'


class VectorSearchType(Enum):
    APPROXIMATE = 'approximate'
    EXACT = 'exact'


class TextRankingStrategy(Enum):
    BM25 = 'bm25'
    SEMANTIC = 'semantic'


class VectorRankingStrategy(Enum):
    COSINE = 'cosine'
    # EUCLIDEAN = 'euclidean'
    # DOT_PRODUCT = 'dot_product'


class ReRankingStrategy(Enum):
    RRF = 'rrf'  # Reciprocal Rank Fusion
    SEMANTIC = 'semantic'


class AzureAISearchEngine(SearchEngine):
    """
    Class to search a text with Azure AI Search
    """
    _service_endpoint: str
    _key: str
    _index_name: str
    _semantic_search_config_name: str = None
    search_client: SearchClient = None
    search_index_client: SearchIndexClient = None

    def __init__(
        self,
        service_endpoint: str = None,
        key: str = None,
        index_name: str = None,
        semantic_search_config_name: str = None
    ):
        logging.info("Start AzureAISearch configuration ...")

        self._service_endpoint = service_endpoint if service_endpoint \
            else os.getenv(ENV_KEY_SEARCH_ENGINE_AISEARCH_ENDPOINT)
        self._key = key if key \
            else os.getenv(ENV_KEY_SEARCH_ENGINE_AISEARCH_KEY)
        self._index_name = index_name if index_name \
            else os.getenv(ENV_KEY_SEARCH_ENGINE_AISEARCH_INDEX_NAME)
        self._semantic_search_config_name = semantic_search_config_name

        # log configuration
        logging.info(f"Azure AI Search service_endpoint: \
            {self._service_endpoint}")
        logging.info(f"Azure AI Search key: {mask_key(self._key, 2, -2)}")
        logging.info(f"Azure AI Search index_name: {self._index_name}")

        logging.info("Completed AzureAISearch configuration.")

    def _init_search_client(
        self,
        index_name: str = None,
        force: bool = False
    ) -> None:
        """
        Initialize search client
        """
        logging.info("Start search client initialization...")
        if force \
            or self.search_client is None \
                or (index_name and self._index_name != index_name):
            logging.info("Initialize search client...")
            if index_name and self._index_name != index_name:
                self._index_name = index_name
            credential = AzureKeyCredential(self._key)
            self.search_client = SearchClient(
                self._service_endpoint,
                self._index_name,
                credential
            )
            logging.info("Completed search client initialization.")
        else:
            logging.info("Completed search client initialization: \
                search client is already initialized.")

    def _init_search_index_client(self, force: bool = False) -> None:
        """
        Initialize search index client
        """
        logging.info("Start search index client initialization...")
        if force or self.search_index_client is None:
            logging.info("Initialize search index client...")
            credential = AzureKeyCredential(self._key)
            self.search_index_client = SearchIndexClient(
                self._service_endpoint,
                credential
            )
            logging.info("Completed search index client initialization.")
        else:
            logging.info("Completed search index client initialization: \
                search index client is already initialized.")

    def search(self, text: str) -> Iterable:
        """
        Search text
        @param text: search text
        @return: search results
        """
        logging.info("Start search text...")

        # initialize search client (if not already initialized)
        self._init_search_client()

        results = self.search_client.search(search_text=text)
        response_list = [r for r in results]

        logging.info(f"Completed search text. \
            Sorted results has {len(response_list)}")
        return response_list

    def _search_text(
        self,
        text: str,
        text_search_type: TextSearchType = TextSearchType.SIMPLE,
        text_ranking_strategy: TextRankingStrategy = TextRankingStrategy.BM25
    ) -> Iterable:
        logging.info("Start text search ...")

        # initialize search client if not initialized already
        self.__init_search_client()

        # common parameters
        kwargs = {
            'search_text': text,
            'search_fields': SEARCH_FIELDS,
            'select': SELECT_FIELDS,
            'top': NUMBER_OF_NEIGHBORS_FOR_TEXT_SEARCH,
            # 'include_total_count': True
        }

        # search type specific parameters
        match text_search_type:
            case TextSearchType.SIMPLE:
                kwargs['query_type'] = 'simple'
            case TextSearchType.FULL:
                kwargs['query_type'] = 'full'
                kwargs['search_mode'] = 'any'
            case _:
                raise ValueError(f"Invalid search type: {text_search_type}")

        # ranking strategy specific parameters
        match text_ranking_strategy:
            case TextRankingStrategy.BM25:
                pass
            case TextRankingStrategy.SEMANTIC:
                kwargs['query_type'] = 'semantic'
                # kwargs['query_language'] = QUERY_LANGUAGE
                kwargs['semantic_configuration_name'] = \
                    self._semantic_search_config_name

        # search
        logging.info(f"Start search ...: {kwargs}")
        search_results = self.search_client.search(**kwargs)

        # log total count if requested
        if kwargs.get('include_total_count'):
            try:
                logging.info(f"Search results has approx. \
                    {search_results.get_count()} items.")
            except Exception as err:
                logging.error("Error getting count: ", err)

        # rank search results
        match text_ranking_strategy:
            case TextRankingStrategy.BM25:
                response_list = [r for r in search_results]
                results = sorted(
                    [r for r in response_list],
                    key=lambda r: r['@search.score'],
                    reverse=True
                )
            case TextRankingStrategy.SEMANTIC:
                response_list = [r for r in search_results]
                results = sorted(
                    [r for r in response_list],
                    key=lambda r: r['@search.reranker_score']
                    if r['@search.reranker_score'] is not None
                    else DEFAULT_SEMANTIC_SCORE_VALUE,
                    reverse=True
                )
            case _:
                raise ValueError(f"Invalid ranking strategy: \
                    {text_ranking_strategy}")

        logging.info(f"Completed text search. \
            Sorted results has {len(results)} items.")
        return results

    def _search_vector(
        self,
        vector: list,
        vector_fields: str = VECTOR_FIELDS,
        vector_search_type: VectorSearchType = VectorSearchType.APPROXIMATE,
        vector_ranking_strategy: VectorRankingStrategy = VectorRankingStrategy.COSINE  # noqa: E501
    ) -> list:
        """
        Search vector
        @param vector: vector input
        @param vector_fields: fields to search
        @param search_type: search type
        @param vector_ranking_strategy: ranking strategy
        @return: search results
        """
        logging.info("Start search vector ...")

        # initialize search client if not initialized already
        self.__init_search_client()

        kwargs = {
            'search_text': None,
            # 'vector': vector,
            # 'vector_fields': vector_fields,
            # 'top_k': NUMBER_OF_NEIGHBORS_FOR_VECTOR_SEARCH,
            'select': SELECT_FIELDS,
            # 'include_total_count': True
        }

        is_exhaustive: bool = None
        match vector_search_type:
            case VectorSearchType.APPROXIMATE:
                is_exhaustive = False
            case VectorSearchType.EXACT:
                is_exhaustive = True
            case _:
                raise ValueError(f"Invalid search type: {vector_search_type}")

        vector_query = VectorizedQuery(
            vector=vector,
            k=NUMBER_OF_NEIGHBORS_FOR_VECTOR_SEARCH,
            fields=vector_fields,
            exhaustive=is_exhaustive
        )
        kwargs['vector_queries'] = [vector_query]

        # search
        logging.info(f"Start search ...: {kwargs}")
        search_results = self.search_client.search(**kwargs)

        # log total count if requested
        if kwargs.get('include_total_count'):
            try:
                logging.info(f"Search results has approx. \
                    {search_results.get_count()} items.")
            except Exception as err:
                logging.error("Error getting count: ", err)

        # rank search_results
        # TODO
        response_list = [r for r in search_results]
        results = sorted(
            [r for r in response_list],
            key=lambda r: r['@search.score'],
            reverse=True
        )

        logging.info(f"Completed search vector. \
            Sorted results has {len(results)} items.")
        return results

    def _search_hybrid(
        self,
        text: str,
        vector: list,
        vector_fields: str = VECTOR_FIELDS,
        text_search_type: TextSearchType = TextSearchType.SIMPLE,
        text_ranking_strategy: TextRankingStrategy = TextRankingStrategy.BM25,
        vector_search_type: VectorSearchType = VectorSearchType.APPROXIMATE,
        vector_ranking_strategy: VectorRankingStrategy = VectorRankingStrategy.COSINE,  # noqa: E501
        re_ranking_strategy: ReRankingStrategy = ReRankingStrategy.RRF
    ) -> list:
        """
        Search text
        @param text: search text
        @param vector: vector input
        @param search_type: search type, default is SearchType.APPROXIMATE
        @param ranking_strategy: ranking strategy, default is BM25
        @return: search results
        """
        logging.info("Start search text ...")

        # initialize search client if not initialized already
        self.__init_search_client()

        vector_query = VectorizedQuery(
            vector=vector,
            k=NUMBER_OF_NEIGHBORS_FOR_VECTOR_SEARCH,
            fields=vector_fields
        )

        # common parameters
        kwargs = {
            'search_text': text,
            'search_fields': SEARCH_FIELDS,
            'top': NUMBER_OF_NEIGHBORS_FOR_TEXT_SEARCH,
            'vector_queries': [vector_query],
            # 'vector': vector,
            # 'vector_fields': vector_fields,
            # 'top_k': NUMBER_OF_NEIGHBORS_FOR_VECTOR_SEARCH,
            'select': SELECT_FIELDS,
            # 'include_total_count': True
        }

        # search type specific parameters
        match text_search_type:
            case TextSearchType.SIMPLE:
                kwargs['query_type'] = 'simple'
            case TextSearchType.FULL:
                kwargs['query_type'] = 'full'
                kwargs['search_mode'] = 'any'
            case _:
                raise ValueError(f"Invalid search type: {text_search_type}")

        # ranking strategy specific parameters
        match text_ranking_strategy:
            case TextRankingStrategy.BM25:
                pass
            case TextRankingStrategy.SEMANTIC:
                kwargs['query_type'] = 'semantic'
                # kwargs['query_language'] = QUERY_LANGUAGE
                kwargs['semantic_configuration_name'] = \
                    self.semantic_search_config_name

        # search
        logging.info(f"Start search ...: {kwargs}")
        search_results = self.search_client.search(**kwargs)

        # log total count if requested
        if kwargs.get('include_total_count'):
            try:
                logging.info(f"Search results has approx. \
                    {search_results.get_count()} items.")
            except Exception as err:
                logging.error("Error getting count: ", err)

        # re-rank search results
        match re_ranking_strategy:
            case None:
                results = [r for r in search_results]
            case ReRankingStrategy.RRF:
                response_list = [r for r in search_results]
                results = sorted(
                    [r for r in response_list],
                    key=lambda r: r['@search.score'],
                    reverse=True
                )
            case ReRankingStrategy.SEMANTIC:
                response_list = [r for r in search_results]
                results = sorted(
                    [r for r in response_list],
                    key=lambda r: r['@search.reranker_score']
                    if r['@search.reranker_score'] is not None
                    else DEFAULT_SEMANTIC_SCORE_VALUE,
                    reverse=True
                )
            case _:
                raise ValueError(f"Invalid re-ranking strategy: \
                    {re_ranking_strategy}")

        logging.info(f"Completed search text. \
            Sorted results has {len(results)} items.")
        return results

    def create_index(self, index_name: str, schema: dict) -> SearchIndex:
        """
        Create empty index
        @param name: index name
        @param documents: document list
        @return: None
        """
        logging.info(f"Start creating index '{index_name}'...")

        # initialize search index client (if not already initialized)
        self._init_search_index_client()

        # assuming one profile per index
        vector_search_profile_name = f"{index_name}-profile"
        has_vector_field = False
        fields = []
        for item_key, item_value in schema.items():
            field_name = item_key
            data_type = SEARCH_FIELD_DATA_TYPE_MAPPING.get(
                item_value.get('data_type', 'string'))
            key = item_value.get('key', False)
            searchable = item_value.get('searchable', False)
            vector_search_dimensions = item_value.get(
                'vector_search_dimensions', None)
            if vector_search_dimensions and vector_search_profile_name:
                has_vector_field = True
            # collection = item_value.get('collection', False)
            field_type = FIELD_TYPE_MAPPING.get(
                item_value.get('field_type', SimpleField))
            field_vector_search_profile_name = vector_search_profile_name \
                if has_vector_field else None
            field = field_type(
                name=field_name,
                type=data_type,
                key=key,
                # collection=collection,
                searchable=searchable,
                vector_search_dimensions=vector_search_dimensions,
                vector_search_profile_name=field_vector_search_profile_name
            )
            fields.append(field)

        if has_vector_field:
            # assumed 1 vector algo per index
            vector_algo_config_name = f"{index_name}-myHnsw"
            vector_search = VectorSearch(
                algorithms=[HnswAlgorithmConfiguration(
                    name=vector_algo_config_name
                )],
                profiles=[
                    VectorSearchProfile(
                        name=vector_search_profile_name,
                        algorithm_configuration_name=vector_algo_config_name,
                    )
                ]
            )
        else:
            vector_search = None

        cors_options = CorsOptions(
            allowed_origins=["*"],
            max_age_in_seconds=60
        )
        scoring_profiles: List[ScoringProfile] = []

        index = SearchIndex(
            name=index_name,
            fields=fields,
            cors_options=cors_options,
            scoring_profiles=scoring_profiles,
            vector_search=vector_search
        )
        search_index = self.search_index_client.create_index(index)

        logging.info(f"Completed creating index '{search_index.name}' \
            with {len(fields)} fields.")
        return search_index

    def upload_documents(self, index_name: str, documents: List[Dict]):
        logging.info(f"Start adding {len(documents)} documents \
            to index '{index_name}'...")

        # initialize search client (if not already initialized)
        self._init_search_client(index_name=index_name)

        result = self.search_client.upload_documents(documents=documents)

        logging.info(f"Completed adding {len(documents)} documents \
            to index '{index_name}'.")

        logging.info(f"result {result}")
        return result
