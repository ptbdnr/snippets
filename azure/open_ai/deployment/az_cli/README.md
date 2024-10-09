# Deploy model

## Requirements

* Azure subscription
* Azure CLI: to sing-in to the Azure account

```shell
# Azure CLI expected version: 2.61 or higher
az --version
```

## Create Azure resource
ref. https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=cli

1. Create a Resource Group

```shell
az group create \ 
    --name $RESOURGE_GROUP_NAME \ 
    --location $LOCATION
```

2. Create a Cognitiveservices resource

```shell
az cognitiveservices account create \ 
    --resource-group $RESOURGE_GROUP_NAME \ 
    --location $LOCATION \ 
    --kind OpenAI \ 
    --sku s0 \ 
    --name $OPENAI_RESOURCE_NAME \ 
```

Access the endpoint URL and API key, this requires jq JSON processor.

```shell
az cognitiveservices account show \ 
    --resource-group $RESOURGE_GROUP_NAME \ 
    --name $OPENAI_RESOURCE_NAME \ 
    | jq -r .properties.endpoint

az cognitiveservices account keys list \ 
    --resource-group $RESOURGE_GROUP_NAME \ 
    --name $OPENAI_RESOURCE_NAME \ 
    | jq -r .key1
```

3. Deploy a model

| MODEL_NAME | MODEL_VERSION |
| gpt-35-turbo | 0613 |
| gpt-35-turbo | 1106 |
| gpt-35-turbo | 0125 |
| gpt-4 | 0613 |
| gpt-4 | turbo-2024-04-09 |
| gpt-4-32k | 0613 |
| gpt-4o | 2024-05-13 |
| gpt-4o | 2024-08-06 |
| gpt-4o-mini | 2024-07-18 |
| test-embedding-ada-002 | 2 |

SKU_NAME is subject to model and version and must be one of: `Standard`, `GlobalBatch`, `GlobalStandard`, and `ProvisionedManaged`
SKU_CAPACITY is an integer representing 1000 units, eg 50 = 50K

```shell
az cognitiveservices account deployment create \ 
    --resource-group  $RESOURGE_GROUP_NAME \ 
    --name $OPENAI_RESOURCE_NAME \ 
    --deployment-name $DEPLOYMENT_NAME \ 
    --model-format OpenAI \ 
    --model-name $MODEL_NAME \ 
    --model-version $MODEL_VERSION \ 
    --sku-name $SKU_NAME \ 
    --sku-capacity $SKU_CAPACITY
```