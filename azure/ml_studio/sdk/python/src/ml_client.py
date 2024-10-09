# References:
# * https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script  # noqa E501

import os
from azure.ai.ml import MLClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import InteractiveBrowserCredential

ENV_KEY_AZURE_TENANT_ID = "AZURE_TENANT_ID"
ENV_KEY_AZURE_SUBSCRIPTION_ID = "AZURE_SUBSCRIPTION_ID"
ENV_KEY_AZURE_RESOURCE_GROUP_NAME = "AZURE_RESOURCE_GROUP_NAME"  # noqa E501
ENV_KEY_AZURE_ML_WORKSPACE_NAME = "AZURE_ML_WORKSPACE_NAME"

tenant_id = os.getenv(ENV_KEY_AZURE_TENANT_ID)
subscription_id = os.getenv(ENV_KEY_AZURE_SUBSCRIPTION_ID)
resource_group_name = os.getenv(ENV_KEY_AZURE_RESOURCE_GROUP_NAME)
ml_workspace_name = os.getenv(ENV_KEY_AZURE_ML_WORKSPACE_NAME)

credential = InteractiveBrowserCredential(tenant_id=tenant_id)
        
ml_client = MLClient(
    credential=credential,
    subscription_id=subscription_id,
    resource_group_name=resource_group_name,
    workspace_name=ml_workspace_name,
)