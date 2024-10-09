"""
# Deploy model as a serverless API with subscription

## Requirements

* Azure subscription
* Azure Machine Learning SDK for Python

```shell
pip install azure-ai-ml
```

## Deploy an AI model as a serverless API with subscription
ref. https://learn.microsoft.com/en-us/azure/ai-studio/how-to/deploy-models-serverless?tabs=python
status: in preview (9 Oct 2024)

Not all AI models on Azure support this deployment process.
This process requires multiple criteria:
1) The model on Azure must support the deployment option: "Serverless API"
2) The model card on Azure must surface a ModelId
4) Available only to users whose Azure subscription belongs to a billing account in a country where the model provider has made the offer available. And the model is to be deployed in a region where it is enabled See https://learn.microsoft.com/en-us/azure/ai-studio/how-to/deploy-models-serverless-availability 
    * Error: `MarketplaceSubscriptionpurchaseEligibilityCheckFailed` Message: Marketplace Subscription purchase eligibility check failed, error message [The purchasing store is not eligible for purchase of this offer due to Second Party store restrictions. Please verify the offer has the tag "hideFromSaasBlade" set to true.].
    * Error: `MarketplacePlanNotRequiredForModel` Message: Marketplace plan is not required for ModelId $MODEL_ID

ModelId example, tested on 9 Oct 2024: `azureml://registries/azureml-meta/models/Meta-Llama-3-8B-Instruct`

Prerequisites:
1. Create a Resource Group
2. Create a Machine Learning workspace (project)
"""

# 3. Configure the `ml` az cli extension for Azure Machine Learning

import os
import dotenv
dotenv.load_dotenv()

TENANT_ID = os.getenv("AZURE_TENANT_ID")
SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
RESOURCE_GROUP_NAME = os.getenv("AZURE_RESOURCE_GROUP_NAME")
ML_WORKSPACE_NAME = os.getenv("AZURE_ML_WORKSPACE_NAME")


from azure.ai.ml import MLClient
from azure.identity import InteractiveBrowserCredential
from azure.ai.ml.entities import MarketplaceSubscription, ServerlessEndpoint

credential = InteractiveBrowserCredential(tenant_id=TENANT_ID)
client = MLClient(
    credential=credential,
    subscription_id=SUBSCRIPTION_ID,
    resource_group_name=RESOURCE_GROUP_NAME,
    workspace_name=ML_WORKSPACE_NAME
)

# 4. Subsribe to the serverless API of the model
# Identify the model name and model ID on Azure AI Studio, and define a deployment name. Example:
# model_id="azureml://registries/azureml-meta/models/Meta-Llama-3-8B-Instruct"
# subscription_name="Meta-Llama-3-8B-Instruct"

SUBSCRIPTION_NAME = os.getenv("SUBSCRIPTION_NAME")
MODEL_ID = os.getenv("MODEL_ID")


# Create a new subscription
marketplace_subscription = MarketplaceSubscription(
    name=SUBSCRIPTION_NAME,
    model_id=MODEL_ID,
)

marketplace_subscription = client.marketplace_subscriptions.begin_create_or_update(
    marketplace_subscription
).result()

# Verify the subscription
marketplace_sub_list = client.marketplace_subscriptions.list()

for sub in marketplace_sub_list:
    print(sub.as_dict())

# 5. Deploy the model to a serverless API endpoint

ENDPOINT_NAME = os.getenv("ENDPOINT_NAME")

serverless_endpoint = ServerlessEndpoint(
    name=ENDPOINT_NAME,
    model_id=MODEL_ID
)

created_endpoint = client.serverless_endpoints.begin_create_or_update(
    serverless_endpoint
).result()

# Get keys (primary and secondary)
endpoint_keys = client.serverless_endpoints.get_keys(ENDPOINT_NAME)
print(endpoint_keys.primary_key)
print(endpoint_keys.secondary_key)

# 5. Delete an endpoint and subscription

# Delete endpoint deployment
client.serverless_endpoints.begin_delete(ENDPOINT_NAME).wait()

# Delete subscription
client.marketplace_subscriptions.begin_delete(SUBSCRIPTION_NAME).wait()

"""
Next: 5. Delete the resource
"""