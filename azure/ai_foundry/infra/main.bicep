targetScope = 'resourceGroup'

// ********************************************
// PARAMETERS
// ********************************************

@description('Location for all resources')
param rLocation string

@description('Managed Identity Id (for example for Function App)`)
param identityId string

// ********************************************
// VARIABLES
// ********************************************

var rNamePrefix = 'foo'
var rNameSuffix = 'bar'

// https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/role-based-access-control
var cognitiveServicesContributorRoleId = '25fbc0a9-bd7c-42a3-aa1a-3b75d497ee68'

func addPrefixAndSuffix(name string) string => '${rNamePrefix}-${name}-${rNameSuffix}'

// ********************************************
// NEW RESOURCES
// ********************************************

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

// ********************************************
// ROLE ASSIGNMENT
// ********************************************

// Grant the Identity a read+write permission to Cognitive Services (for OpenAI)
resource roleAssignmentCognitiveServices 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().id, identityId,  'Cognitive Services Contributor')
  scope: resourceGroup()
  properties: {
    principalType: 'ServicePrincipal'
    principalId: identityId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', cognitiveServicesContributorRoleId)
  }
}
