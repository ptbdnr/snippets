// Parameters
// @description('Name of the resource group where all resources will be created.')
// param resourceGroupName string

@description('Location for all resources.')
param location string

@description('Name of the virtual network.')
param vnetName string

@description('Name of the subnet.')
param subnetName string

@description('Name of the storage account.')
param storageAccountName string

@description('Name of the private endpoint.')
param privateEndpointName string

@description('Name of the private DNS zone.')
param privateDnsZoneName string

@description('Name of the app service plan.')
param appServicePlanName string

@description('Name of the function app.')
param functionAppName string


// Create Resource Group
// targetScope = 'subscription'
// resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
//   name: resourceGroupName
//   location: location
// }

// Create Virtual Network with Subnet
targetScope = 'resourceGroup'
resource virtualNetwork 'Microsoft.Network/virtualNetworks@2021-02-01' = {
  name: vnetName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
    subnets: [
      {
        name: subnetName
        properties: {
          addressPrefix: '10.0.0.0/24'
        }
      }
    ]
  }
}

// Create Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2021-04-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
  }
}

// Create Private Endpoint for Storage Account
resource privateEndpoint 'Microsoft.Network/privateEndpoints@2021-05-01' = {
  name: privateEndpointName
  location: location
  properties: {
    subnet: {
      id: virtualNetwork.properties.subnets[0].id
    }
    privateLinkServiceConnections: [
      {
        name: 'storageAccountConnection'
        properties: {
          privateLinkServiceId: storageAccount.id
          groupIds: [
            'blob'
          ]
        }
      }
    ]
  }
}

// Create Private DNS Zone
resource privateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: privateDnsZoneName
  location: 'global'
}

// Link Private DNS Zone to Virtual Network
resource privateDnsZoneVnetLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  name: 'dnsLink'
  parent: privateDnsZone
  properties: {
    virtualNetwork: {
      id: virtualNetwork.id
    }
    registrationEnabled: false
  }
}

// Create DNS A Record in Private DNS Zone
resource dnsARecord 'Microsoft.Network/privateDnsZones/A@2020-06-01' = {
  name: '${storageAccountName}.${privateDnsZoneName}'
  parent: privateDnsZone
  properties: {
    ttl: 3600
    aRecords: [
      {
        ipv4Address: privateEndpoint.properties.networkInterfaces[0].properties.ipConfigurations[0].properties.privateIPAddress
      }
    ]
  }
}

// Create App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2021-02-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  properties: {
    reserved: true
  }
}

// Create Function App
resource functionApp 'Microsoft.Web/sites@2021-02-01' = {
  name: functionAppName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'python|3.11'
      appSettings: [
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccountName};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net'
        }
      ]
    }
  }
  kind: 'functionapp,linux'
  dependsOn: [
    // appServicePlan
    // storageAccount
    privateEndpoint
    privateDnsZone
    privateDnsZoneVnetLink
    dnsARecord
  ]
}

// Enable VNet Integration for Function App
resource vnetIntegration 'Microsoft.Web/sites/virtualNetworkConnections@2021-02-01' = {
  parent: functionApp
  name: 'vnet'
  properties: {
    vnetResourceId: virtualNetwork.properties.subnets[0].id
  }
  dependsOn: [
    // functionApp
  ]
}
