targetScope = 'resourceGroup'

// ********************************************
// PARAMETERS
// ********************************************

@description('Project Name')
param projectName string

@description('Environment')
param environment string

@description('Location for all resources')
param rLocation string

@description('Subnet ID for the datastore')
param subnetId string

@description('Itentity ID of the principal/user')
param identityId string

// ********************************************
// VARIABLES
// ********************************************

var rgProjectName = projectName
var rgNameSuffix = environment

func addPrefixAndSuffix(name string) string => '${name}-${rgProjectName}-${rgNameSuffix}'

// ********************************************
// AI SERVICES
// ********************************************

// Azure Document Intelligence
resource docIntel 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: addPrefixAndSuffix('docintel')
  location: rLocation
  kind: 'FormRecognizer'
  identity: { type: 'SystemAssigned' }
  sku: { name: 'S0' }
  properties: {
    customSubDomainName: addPrefixAndSuffix('docintel')
    publicNetworkAccess: 'Enabled' // TODO: 'Disabled'
    networkAcls: {
      defaultAction: 'Allow' // TODO: 'Deny'
      virtualNetworkRules: [
        {
          id: subnetId
          ignoreMissingVnetServiceEndpoint: false
        }
      ]
    }
  }
}

// ********************************************
// KEYS
// ********************************************

resource keyVault 'Microsoft.KeyVault/vaults@2024-12-01-preview' = {
  name: addPrefixAndSuffix('kv')
  location: rLocation
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    networkAcls: { 
      bypass: 'AzureServices'
      defaultAction: 'Allow' // TODO: 'Deny'
      ipRules: []
      virtualNetworkRules: [
        {
          id: subnetId
          ignoreMissingVnetServiceEndpoint: false
        }
      ]
    }
    accessPolicies: [
      {
        objectId: identityId
        tenantId: subscription().tenantId
        permissions: {
          keys: ['get', 'list']
          secrets: ['get', 'list']
        }
      }
    ]
  }
}

// Store Document Intelligence API key in Key Vault
resource docIntelApiKeySecret 'Microsoft.KeyVault/vaults/secrets@2024-12-01-preview' = {
  parent: keyVault
  name: 'DocIntelApiKey'
  properties: {
    value: docIntel.listKeys().key1
  }
}

// ********************************************
// OUTPUTS
// ********************************************

output docintel_endpoint string = docIntel.properties.endpoint
output docIntelName string = docIntel.name
