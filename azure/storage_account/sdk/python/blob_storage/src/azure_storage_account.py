import os
import logging
from types import List

from azure.storage.blob import BlobServiceClient

from src.storage import Storage
from src.encrypt import mask_key

KEY_ENV_STORAGE_AZURE_STORAGE_ACCOUNT_CONNECTION_STRING = 'STORAGE_AZURE_STORAGE_ACCOUNT_CONNECTION_STRING'


class AzureStorageAccount(Storage):
    """
    Azure Storage Account wrapper
    """
    blob_service_client: BlobServiceClient

    def __init__(self,
                 connection_string: str = None,
                 ):
        logging.info("Start AzureStorageAccount configuration ...")

        # Create a BlobServiceClient 
        # using your Azure Storage account connection string
        connection_string = connection_string if connection_string \
            else os.getenv(KEY_ENV_STORAGE_AZURE_STORAGE_ACCOUNT_CONNECTION_STRING)

        # log configuration
        logging.info(f"Azure Storage Account connection_string: \
            {mask_key(connection_string, 2, -2)}")

        # Download the blob with alternative words (in JSON array)
        self.blob_service_client = BlobServiceClient.from_connection_string(
            connection_string,
            # credential=credentials
        )

        logging.info("Completed AzureStorageAccount configuration.")

    def list_containers(self) -> List[str]:
        """
        List all containers
        @return: list of container names
        """
        return self.blob_service_client.list_containers()

    def download_to_text(self, path: str, filename: str) -> str:
        """
        Return data in text
        @param path: container name
        @filename: filename
        @return: text content
        """
        logging.info(f"Start downloading {path}/{filename} to inputstream...")

        blob_client = self.blob_service_client.get_blob_client(
            container=path,
            blob=filename
        )
        downloader = blob_client.download_blob(
            max_concurrency=1,
            encoding='UTF-8'
        )
        blob_text = downloader.readall()

        logging.info(f"Completed downloading {path}/{filename} \
            to inputstream.")
        return blob_text
