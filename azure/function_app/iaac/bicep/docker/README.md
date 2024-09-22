# IaaC with Azure Bicep


## Requirements

* Azure subscription
* Azure CLI: to sing-in to the Azure account
* Azure Bicep

```shell
# Azure CLI expected version: 2.61 or higher
az --version
# Azure Bicep expected version: v0.30.x or higher
az bicep version
```

## Create Azure resources

1. Create a Resource Group

Definition uses `Microsoft.Resources/resourceGroups`

2. Create a Container Registry

Definition uses `Microsoft.ContainerRegistry/registries`

3. Create a Storage Account

This is used by the Function App.

Definition uses `Microsoft.Storage/storageAccounts`

4. Create an App Service Plan

This hosts the Function App

Definition uses `Microsoft.Web/serverfarms`

5. Create an Azure Function App
`Microsoft.Web/sites`

Docker image deployment may take several minutes.

Remember to configure CORS as appropriate.


You can deploy this Bicep template using the Azure CLI:

ref: https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-cli

ref: https://learn.microsoft.com/en-us/cli/azure/deployment/group?view=azure-cli-latest#az-deployment-group-create


```shell
az deployment group create \ 
    --resource-group $RESOURCE_GROUP_NAME \ 
    --name 'myDeployment-'$(date +"%Y-%b-%d")
    --template-file $PATH_TO_BICEP_FILE \ 
    --parameters $PATH_TO_BICEPPARAM_FILE 
```