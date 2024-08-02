import logging

from src.data_store import DataStore


class MockupDataStore(DataStore):
    """
    Mockup class for data store.
    """

    item_list = [{
        "id": "FOO",
        "key": "FOO",
        "definition": "FOO is BAR and BUZ"
    }]

    def insert_item(self, item: dict):
        pass

    def read_items(self, max_item_count: int) -> list:
        return self.item_list[:max_item_count]

    def query_items(self, field_name_value: dict) -> list:
        """
        Query records
        @param field_name_value: dictionary with key = field name
            and value = field value
        @return: list of records
        """
        logging.info(f"Start {type(self).__name__}().query_items ...")

        item_list = self.item_list

        logging.info(f"Completed {type(self).__name__}().query_items. \
            Returned {item_list.__len__()} items.")
        return item_list
