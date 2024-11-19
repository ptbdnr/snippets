## Workspace setup
install python3.10: https://www.python.org/downloads/release/python-3100/

Create a new folder on your local computer.

Create an environment 

on Unix:
```bash
python3.10 -m venv .venv
source .venv/bin/activate
```
on Windows
```batch
python3.10 -m venv .venv
.venv/Scripts/activate.bat
```

install azure-storage-blob
```bash
pip install --upgrade pip
pip install azure-identity 
pip install azure-storage-blob
```

## Use the SDK

In Azure Portal, click on the search bar.
Search and select the service: `Storage accounts`.
Select and click on a storage account name.
In the navigation menu find the group named `Settings` and select `Endpoints`. 
Then under section Blob service find the primary endpoint and the Blob service. 
Save this in a local environment variable.

on Unix:
```bash
export STORAGE_ACCOUNT_URL=https://[STORAGE_ACCOUNT_NAME].blob.core.windows.net/
```
on Windows:
```batch
set STORAGE_ACCOUNT_URL=https://[STORAGE_ACCOUNT_NAME].blob.core.windows.net/
```

then run the following to list the containers in the account
```bash
python3.10 -c "import os; from azure.identity import DefaultAzureCredential; from azure.storage.blob import BlobServiceClient; [print(c['name']) for c in BlobServiceClient(os.environ['STORAGE_ACCOUNT_URL'], DefaultAzureCredential()).list_containers()]"
```