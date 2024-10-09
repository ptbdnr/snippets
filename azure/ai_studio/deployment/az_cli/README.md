# Deploy model

## Requirements

* Azure subscription
* Azure CLI: to sing-in to the Azure account
* ml extension for Azure Machine Learning `az extension add -n ml`

```shell
# Azure CLI expected version: 2.61 or higher
az --version
# Azure CLI ML extension expected version: v2 or higher
az ml -h
```

## Deploy an AI model as a serverless API with subscription
ref. https://learn.microsoft.com/en-us/azure/ai-studio/how-to/deploy-models-serverless?tabs=cli
status: in preview (9 Oct 2024)

Not all AI models on Azure support this deployment process.
This process requires multiple criteria:
1) The model on Azure must support serverless API deployment mode
2) The model card on Azure must surface a ModelId
4) Available only to users whose Azure subscription belongs to a billing account in a country where the model provider has made the offer available. And the model is to be deployed in a region where it is enabled See https://learn.microsoft.com/en-us/azure/ai-studio/how-to/deploy-models-serverless-availability 
    * Error: `MarketplaceSubscriptionpurchaseEligibilityCheckFailed` Message: Marketplace Subscription purchase eligibility check failed, error message [The purchasing store is not eligible for purchase of this offer due to Second Party store restrictions. Please verify the offer has the tag "hideFromSaasBlade" set to true.].
    * Error: `MarketplacePlanNotRequiredForModel` Message: Marketplace plan is not required for ModelId $MODEL_ID

ModelId example, tested on 9 Oct 2024: `azureml://registries/azureml-meta/models/Meta-Llama-3-8B-Instruct`


1. Create a Resource Group

```shell
az group create \ 
    --name $RESOURGE_GROUP_NAME \ 
    --location $LOCATION \ 
    --tags Owner=$USERNAME
```

2. Create a Machine Learning workspace (project)

```shell
az ml workspace create \ 
    --resource-group $RESOURGE_GROUP_NAME \ 
    --location $LOCATION \ 
    --name $ML_WORKSPACE_NAME 
```

This will create 
* 1x Storage Account
* 1x Key Vault
* 1x Log Analytics Workspace
* 1x Azure ML Workspace


3. Configure the `ml` az cli extension for Azure Machine Learning

```shell
az configure --defaults \ 
    group=$RESOURGE_GROUP_NAME \ 
    location=$LOCATION \ 
    workspace=$ML_WORKSPACE_NAME
# Verify
az configure -l -o table
```

4. Subsribe to the serverless API of the model

Identify the model name and model ID on Azure AI Studio, and define a deployment name. Example:

```plaintext
$SUBSCRIPTION_NAME=Meta-Llama-3-8B-Instruct-subs
$MODEL_ID=azureml://registries/azureml-meta/models/Meta-Llama-3-8B-Instruct
$ENDPOINT_NAME=meta-llama3-8b-mydeployment
```

Save the config and create the subscription

```shell
# Create a new subscription
touch serverless_api_subscription.yml
echo "name: $SUBSCRIPTION_NAME" >> serverless_api_subscription.yml
echo "model_id: $MODEL_ID" >> serverless_api_subscription.yml
az ml marketplace-subscription create -f serverless_api_subscription.yml
# Verify subscription
az ml marketplace-subscription list
```

5. Deploy the model to a serverless API endpoint

```shell
# Create a new endpoint deployment
touch serverless_api_endpoint.yml
echo "name: $ENDPOINT_NAME" >> serverless_api_endpoint.yml
echo "model_id: $MODEL_ID" >> serverless_api_endpoint.yml
az ml serverless-endpoint create -f serverless_api_endpoint.yml
# Verify endpoint deployment
az ml serverless-endpoint list
# URL: https://$DEPLOYMENT_NAME.$LOCATION.models.ai.azure.com
# Get keys (primary and secondary)
az ml serverless-endpoint get-credentials -n $ENDPOINT_NAME
```

5. Delete an endpoint and subscription

```shell
# Delete endpoint deployment
az ml serverless-endpoint delete --name $ENDPOINT_NAME
# Verify endpoint deployment
az ml serverless-endpoint list
# Delete subscription
az ml marketplace-subscription delete --name $SUBSCRIPTION_NAME
# Verify subscription
az ml marketplace-subscription list
```

5. Delete a resource

```shell
az ml workspace delete \ 
    --resource-group $RESOURGE_GROUP_NAME \ 
    --name $ML_WORKSPACE_NAME
```