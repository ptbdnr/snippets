targetScope = 'resourceGroup'

@description('Location for all resources')
param rLocation string

var rNamePrefix = 'foo'
var rNameSuffix = 'bar'

func addPrefixAndSuffix(name string) string => '${main.rgNamePrefix}-${name}-${rNameSuffix}'

resource aiServices 'Microsoft.CognitiveServices/accounts@2024-06-01-preview' = {
  name: addPrefixAndSuffix('aiservices-tmp')
  location: rLocation
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  properties: {
  }
}

resource aiFoundryHub 'Microsoft.MachineLearningServices/workspaces@2024-04-01-preview' = {
  name: addPrefixAndSuffix('aifoundry-hub')
  location: rLocation
  kind: 'Hub'
  sku: {
    name: 'Basic'
    tier: 'Basic'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: addPrefixAndSuffix('aifoundry-hu')
  }

  resource aiServicesConnection 'connections@2024-04-01-preview' = {
    name: addPrefixAndSuffix('aiservices-connection')
    properties: {
      category: 'AIServices'
      target: aiServices.properties.endpoint
      authType: 'AAD'
      isSharedToAll: true
      metadata: {
        ApiType: 'Azure'
        ResourceId: aiServices.id
      }
    }
  }
}

resource aiFoundryProject 'Microsoft.MachineLearningServices/workspaces@2024-04-01-preview' = {
  name: addPrefixAndSuffix('aifoundry-pjct')
  location: rLocation
  kind: 'Project'
  sku: {
    name: 'Basic'
    tier: 'Basic'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: addPrefixAndSuffix('aifoundry-project')
    publicNetworkAccess: 'Enabled'
    hubResourceId: aiFoundryHub.id
  }
}
