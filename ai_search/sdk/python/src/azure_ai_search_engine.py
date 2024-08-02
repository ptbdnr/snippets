import os
import logging
from collections.abc import Iterable
from typing import List, Dict

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
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
ENV_KEY_SEARCH_ENGINE_AISEARCH_ENDPOINT = os.getenv('SEARCH_ENGINE_AISEARCH_ENDPOINT')
ENV_KEY_SEARCH_ENGINE_AISEARCH_KEY = os.getenv('SEARCH_ENGINE_AISEARCH_KEY')
ENV_KEY_SEARCH_ENGINE_AISEARCH_INDEX_NAME = os.getenv('SEARCH_ENGINE_AISEARCH_INDEX_NAME')

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


class AzureAISearchEngine(SearchEngine):
    """
    Class to search a text with Azure AI Search
    """
    _service_endpoint: str
    _key: str
    _index_name: str
    search_client: SearchClient = None
    search_index_client: SearchIndexClient = None

    def __init__(self,
                 service_endpoint: str = None,
                 key: str = None,
                 index_name: str = None,
                 ):
        logging.info("Start AzureAISearch configuration ...")

        self._service_endpoint = service_endpoint if service_endpoint \
            else os.getenv(ENV_KEY_SEARCH_ENGINE_AISEARCH_ENDPOINT)
        self._key = key if key \
            else os.getenv(ENV_KEY_SEARCH_ENGINE_AISEARCH_KEY)
        self._index_name = index_name if index_name \
            else os.getenv(ENV_KEY_SEARCH_ENGINE_AISEARCH_INDEX_NAME)

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
