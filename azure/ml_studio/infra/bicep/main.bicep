@description('Location for all resources.')
param location string = resourceGroup().location

@description('Unique name for the Azure Machine Learning workspace.')
param workspaceName string = 'aml-${uniqueString(resourceGroup().id)}'

@description('Unique name for the storage account name.')
param storageAccountName string = 'sa${uniqueString(resourceGroup().id)}'

@description('Unique name for the Key Vault instance.')
param keyVaultName string = 'kv-${uniqueString(resourceGroup().id)}'

@description('Unique name for the Log Analytics workspace.')
param logAnalyticsName string = 'la-${uniqueString(resourceGroup().id)}'

@description('Unique name for the Application Insights instance.')
param appInsightsName string = 'appi-${uniqueString(resourceGroup().id)}'

@description('Unique name for the container registry.')
param containerRegistryName string = 'acr${uniqueString(resourceGroup().id)}'

@description('Creates a storage account for Azure Machine Learning.')
resource storageAccount 'Microsoft.Storage/storageAccounts@2021-04-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}

@description('Creates a Key Vault for Azure Machine Learning.')
resource keyVault 'Microsoft.KeyVault/vaults@2021-10-01' = {
  name: keyVaultName
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    accessPolicies: []
  }
}

@description('Creates a log analytics workspace for use with Application Insights.')
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2021-12-01-preview' = {
  name: logAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 90
    workspaceCapping: {
      dailyQuotaGb: 1
    }
  }
}

@description('Creates an Application Inslights instance for Azure Machine Learning.')
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalyticsWorkspace.id
  }
}

@description('Creates a container registry for Azure Machine Learning.')
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2022-12-01' = {
  name: containerRegistryName
  location: location
  sku: {
    name: 'Basic'
  }
}

@description('Creates an Azure Machine Learning workspace.')
resource mlWorkspace 'Microsoft.MachineLearningServices/workspaces@2021-07-01' = {
  name: workspaceName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: workspaceName
    storageAccount: storageAccount.id
    keyVault: keyVault.id
    applicationInsights: appInsights.id
    containerRegistry: containerRegistry.id
    description: 'Azure Machine Learning workspace for integration with PostgreSQL'
  }
}

output mlWorkspaceId string = mlWorkspace.id
output azureMLWorkspaceName string = mlWorkspace.name
