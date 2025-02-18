#!/bin/bash

# Update Bicep
az bicep upgrade

# Exit on error
set -e

# Variables
read -p "Enter Azure Tenant ID [None]: " TENANT_ID
# read -p "Enter Azure Subscription ID [None]: " SUBSCRIPTION_ID
read -p "Enter Azure Location (e.g., westus3, uksouth) [uksouth]: " LOCATION
LOCATION=${LOCATION:-swedencentral}
read -p "Enter the stage (e.g., test, prod) [test]: " STAGE
STAGE=${STAGE:-test}
RESOURCE_GROUP_NAME_PREFIX="foo"

# Login to Azure if a Tenant ID is provided
if [ "$TENANT_ID" != "" ]; then
    az login --tenant "$TENANT_ID"
else
    az login
    # az account set --subscription "$SUBSCRIPTION_ID"    
fi

# ########################################
# Deploy the Bicep templates

# main.bicep
echo ""
read -p "Are you sure you want to create the resource groups? (y/N) [No]: " confirmation
TEMPLATE_FILEPATH="main.bicep"
if [[ $confirmation =~ ^[Yy]$ ]]; then
    PARAMETERS_FILEPATH="main.$STAGE.bicepparam"
    az deployment sub create --name $RESOURCE_GROUP_NAME_PREFIX'-'$(date +"%Y-%b-%d") --location $LOCATION --template-file $TEMPLATE_FILEPATH --parameters $PARAMETERS_FILEPATH 
    echo "$TEMPLATE_FILEPATH deployment completed successfully."
else
    echo "Skip: $TEMPLATE_FILEPATH"
fi

# data.bicep
echo ""
read -p "Are you sure you want to create the "DATA" resources? (y/N) [No]: " confirmation
TEMPLATE_FILEPATH="data.bicep"
if [[ $confirmation =~ ^[Yy]$ ]]; then
    RESOURCE_GROUP_NAME="$RESOURCE_GROUP_NAME_PREFIX-data-$STAGE"
    PARAMETERS_FILEPATH="data.$STAGE.bicepparam"
    az deployment group create --name $RESOURCE_GROUP_NAME_PREFIX'-data-'$(date +"%Y-%b-%d") --resource-group $RESOURCE_GROUP_NAME --template-file $TEMPLATE_FILEPATH --parameters $PARAMETERS_FILEPATH 
    echo "$TEMPLATE_FILEPATH deployment completed successfully."
else
    echo "Skip: $TEMPLATE_FILEPATH"
fi

# back.bicep
echo ""
read -p "Are you sure you want to create the "BACK" resources? (y/N) [No]: " confirmation
TEMPLATE_FILEPATH="back.bicep"
if [[ $confirmation =~ ^[Yy]$ ]]; then
    RESOURCE_GROUP_NAME="$RESOURCE_GROUP_NAME_PREFIX-back-$STAGE"
    PARAMETERS_FILEPATH="back.test.bicepparam"
    az deployment group create --name $RESOURCE_GROUP_NAME_PREFIX'-back-'$(date +"%Y-%b-%d") --resource-group $RESOURCE_GROUP_NAME --template-file $TEMPLATE_FILEPATH --parameters $PARAMETERS_FILEPATH 
    echo "$TEMPLATE_FILEPATH deployment completed successfully."
else
    echo "Skip: $TEMPLATE_FILEPATH"
fi

# front.bicep
echo ""
read -p "Are you sure you want to create the "FRONT" resources? (y/N) [No]: " confirmation
TEMPLATE_FILEPATH="front.bicep"
if [[ $confirmation =~ ^[Yy]$ ]]; then
    RESOURCE_GROUP_NAME="$RESOURCE_GROUP_NAME_PREFIX-front-$STAGE"
    PARAMETERS_FILEPATH="front.$STAGE.bicepparam"
    az deployment group create --name $RESOURCE_GROUP_NAME_PREFIX'-front-'$(date +"%Y-%b-%d") --resource-group $RESOURCE_GROUP_NAME --template-file $TEMPLATE_FILEPATH --parameters $PARAMETERS_FILEPATH 
    echo "$TEMPLATE_FILEPATH deployment completed successfully."
else
    echo "Skip: $TEMPLATE_FILEPATH"
fi

echo "----------------------------------"
echo "Deployment completed successfully."
