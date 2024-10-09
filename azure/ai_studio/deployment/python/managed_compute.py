"""
# Deploy model on a managed compute

## Requirements

* Azure Subscription
* Azure Machine Learning SDK for Python
* Virtual Machine quota in the Azure Subscription for model specific SKUs (shared HW is only available for 168hrs):
    * Standard_ND40rs_v2
    * Standard_ND96amsr_A100_v4
    * Standard_ND96asr_v4
    * some model might work with Standard_DS3_v2

```shell
pip install azure-ai-ml
```

## Deploy model on a managed compute
ref. https://learn.microsoft.com/en-us/azure/ai-studio/how-to/deploy-models-managed
ref. for VM SKUs: https://learn.microsoft.com/en-us/azure/machine-learning/concept-model-catalog?view=azureml-api-2
status: in preview (9 Oct 2024)

Not all AI models on Azure support this deployment process.
This process requires multiple criteria:
1) The model on Azure the deployment option: "Managed compute"
2) The model card on Azure must surface a ModelId

ModelId example, tested on 9 Oct 2024: 
`azureml://registries/azureml/models/deepset-roberta-base-squad2/versions/16`

ModelId - VM SKU requirement
azureml://registries/azureml/models/deepset-roberta-base-squad2/versions/16: Standard_DS3_v2
azureml://registries/azureml/models/mistralai-Mistral-7B-Instruct-v0-2/versions/5: Standard_NC12s_v3
azureml://registries/azureml/models/mistralai-Mixtral-8x7B-v01/versions/14: Standard_ND40rs_v2
azureml://registries/azureml-meta/models/Meta-Llama-3-8B/versions/6: Standard_NC12s_v3

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

credential = InteractiveBrowserCredential(tenant_id=TENANT_ID)
client = MLClient(
    credential=credential,
    subscription_id=SUBSCRIPTION_ID,
    resource_group_name=RESOURCE_GROUP_NAME,
    workspace_name=ML_WORKSPACE_NAME
)

# 4. Create an unique endpoint that will point to the managed compute

import uuid
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    ProbeSettings,
)

ENDPOINT_NAME = f"{os.getenv('ENDPOINT_NAME')}-{uuid.uuid4().hex[:5]}"
print(f"ENDPOINT_NAME: {ENDPOINT_NAME}")

# Create an online endpoint
endpoint_config = ManagedOnlineEndpoint(
    name=ENDPOINT_NAME,
    auth_mode="key",
)
client.begin_create_or_update(endpoint_config).wait()


# 5. Create a deployment and update the endpoint (ca 30 min)

MODEL_ID = os.getenv("MODEL_ID")
DEPLOYMENT_NAME = f"{ENDPOINT_NAME}-{uuid.uuid4().hex[:5]}"
print(f"MODEL_ID: {MODEL_ID}")
print(f"DEPLOYMENT_NAME: {DEPLOYMENT_NAME}")

deployment_config = ManagedOnlineDeployment(
    name=DEPLOYMENT_NAME,
    endpoint_name=ENDPOINT_NAME,
    model=MODEL_ID,
    instance_type="Standard_NC24ads_A100_v4",
    instance_count=2,
    liveness_probe=ProbeSettings(
        failure_threshold=30,
        success_threshold=1,
        timeout=2,
        period=10,
        initial_delay=1000,
    ),
    readiness_probe=ProbeSettings(
        failure_threshold=10,
        success_threshold=1,
        timeout=10,
        period=10,
        initial_delay=1000,
    ),
)
client.online_deployments.begin_create_or_update(deployment_config).wait()

# Traffic is the rule to route traffic across deployments.
# In the dict, the key is the deployment name, and value represents the percentage of traffic to that deployment
# ref. https://learn.microsoft.com/en-us/azure/machine-learning/how-to-safely-rollout-online-endpoints?view=azureml-api-2&tabs=python#define-an-endpoint
endpoint_config.traffic = {DEPLOYMENT_NAME: 100}
client.begin_create_or_update(endpoint_config).result()

# 5. Delete an endpoint
# ref. https://learn.microsoft.com/en-us/azure/machine-learning/how-to-safely-rollout-online-endpoints?view=azureml-api-2&tabs=python#remove-the-old-deployment

# Delete endpoint
# client.online_endpoints.begin_delete(name=ENDPOINT_NAME)


"""
Next: 5. Delete the resource
"""