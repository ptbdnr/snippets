// Define parameters

// @description('Name of the resource group.')
// param resourceGroupName string

@description('Location for all resources.')
param location string

@description('Name of the container registry.')
param registryName string

@description('Name of the storage account.')
param storageAccountName string

@description('Name of the app service plan.')
param appServicePlanName string

@description('Name of the function app.')
param functionAppName string

@description('Name of the Docker image. TODO: NOT WORKING IN BICEP, TRY AZ CLI')
param imageName string

@description('Tag of the Docker image.')
param imageTag string = 'latest'

// Create Resource Group
// targetScope = 'subscription'
// resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' = {
//   name: resourceGroupName
//   location: location
// }

targetScope = 'resourceGroup'

// Create Container Registry
// ref https://learn.microsoft.com/en-us/azure/templates/microsoft.containerregistry/registries?pivots=deployment-language-bicep#resource-format
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: registryName
  location: location
  sku: {
    name: 'Standard'
  }
  properties: {
    adminUserEnabled: true
  }
}

// Create Storage Account
// ref: https://learn.microsoft.com/en-us/azure/templates/microsoft.storage/storageaccounts?pivots=deployment-language-bicep#resource-format
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}

// Create App Service Plan
// ref: https://learn.microsoft.com/en-us/azure/templates/microsoft.web/serverfarms?pivots=deployment-language-bicep#resource-format
resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
  kind: 'linux'
  properties: {
    reserved: false
  }
}

// Create Function App
// TODO: NOT WORKING, TRY AZ CLI. ALSO, THE IMAGE SHOULD BE PUSHED TO THE REGISTRY FIRST
// ref: https://learn.microsoft.com/en-us/azure/templates/microsoft.web/sites?pivots=deployment-language-bicep#resource-format
resource functionApp 'Microsoft.Web/sites@2022-09-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp,linux,container'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      // linuxFxVersion: 'PYTHON|3.11'
      // linuxFxVersion: 'DOCKER|${containerRegistry.properties.loginServer}/${imageName}:${imageTag}'
      appSettings: [
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_URL'
          value: 'https://${containerRegistry.properties.loginServer}'
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_USERNAME'
          value: containerRegistry.listCredentials().username
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_PASSWORD'
          value: containerRegistry.listCredentials().passwords[0].value
        }
        { 
          name: 'DOCKER_CUSTOM_IMAGE_NAME' 
          value: '${imageName}:${imageTag}' 
        }
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: 'false'
        }
      ]
    }
  }
  dependsOn: [
    // appServicePlan
    storageAccount
    // containerRegistry
  ]
}
