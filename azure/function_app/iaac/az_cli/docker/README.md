# IaaC with Azure CLI


## Requirements

* Azure subscription
* Azure CLI: to sing-in to the Azure account

```shell
# Azure CLI expected version: 2.61 or higher
az --version
```

## Create Azure resources

1. Create a Resource Group

```shell
az group create 
    --name $RESOURGE_GROUP_NAME 
    --location $LOCATION
```

2. Create a Container Registry

ref: https://learn.microsoft.com/en-us/cli/azure/acr?view=azure-cli-latest#az-acr-create

```shell
az acr create \ 
    --resource-group $RESOURGE_GROUP_NAME \ 
    --name $REGISTRY_NAME \ 
    --sku Standard
    --admin-enabled true
```

3. Create a Storage Account

This is used by the Function App.

ref: https://learn.microsoft.com/en-us/cli/azure/storage/account?view=azure-cli-latest#az-storage-account-create

```shell
az storage account create \ 
    --resource-group $RESOURCE_GROUP_NAME \ 
    --name $STORAGE_NAME \ 
    --sku Standard_LRS
```

4. Create an App Service Plan

This hosts the Function App

ref: https://learn.microsoft.com/en-us/cli/azure/appservice/plan?view=azure-cli-latest#az-appservice-plan-create

```shell
az appservice plan create \ 
    --resource-group $RESOURCE_GROUP_NAME \ 
    --name $APP_PLAN_NAME
```

5. Create an Azure Function App

NB: ClickOps only supports CD from GitHub

ref: https://learn.microsoft.com/en-us/cli/azure/functionapp?view=azure-cli-latest#az-functionapp-create

Docker image deployment may take several minutes.

Remember to configure CORS as appropriate.

This assumes that a Docker image is already deployed within the Azure Continer Registry

```shell
az functionapp create \ 
  --resource-group $RESOURGE_GROUP_NAME \ 
  --plan $APP_PLAN_NAME \ 
  --name $APP_NAME \ 
  --runtime python
  --runtime-version 3.11
  --storage-account $STORAGE_NAME \ 
  --image $LOGIN_SERVER/$IMAGE_NAME:$TAG
```
