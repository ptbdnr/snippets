targetScope = 'resourceGroup'

// ********************************************
// PARAMETERS
// ********************************************

@description('Location for all resources')
param rLocation string

@description('Managed Identity Id (for example for Function App)')
param identityId string

@description('LLM Model Provider, eg. OpenAI')
param llmModelFormat string = 'OpenAI'

@description('LLM Model Name, eg. gpt-4o')
param llmModelName string = 'gpt-4o'

@description('GPT-4o deployment capacity (TPM in thousands)')
param llmModelCapacity int = 10

@description('GPT-4o model version')
param llmModelVersion string = '2024-11-20'

// ********************************************
// VARIABLES
// ********************************************

var rNamePrefix = 'foo'
var rNameSuffix = 'bar'

// https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/role-based-access-control
var cognitiveServicesContributorRoleId = '25fbc0a9-bd7c-42a3-aa1a-3b75d497ee68'

func addPrefixAndSuffix(name string) string => '${rNamePrefix}-${name}-${rNameSuffix}'

// ********************************************
// AI SERVICES FOR LANGUAGE MODEL
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

// Create a custom content filtering configuration with all filters disabled
resource llmNoContentFilter 'Microsoft.CognitiveServices/accounts/raiPolicies@2025-06-01' = {
  parent: aiServices
  name: addPrefixAndSuffix('no-guardrails-policy')
  properties: {
    mode: 'Asynchronous_filter'
    basePolicyName: 'Microsoft.Default'
    contentFilters: [
      {
        name: 'hate'
        severityThreshold: 'High' // ['Low', 'Medium', 'High']
        blocking: true // [true, false] TODO: add permission to override base policy
        // enabled: false
        source: 'Prompt'
      }
      {
        name: 'hate'
        severityThreshold: 'High' // ['Low', 'Medium', 'High']
        blocking: true // [true, false] TODO: add permission to override base policy
        // enabled: false
        source: 'Completion'
      }
      {
        name: 'sexual'
        severityThreshold: 'High' // ['Low', 'Medium', 'High']
        blocking: true // [true, false] TODO: add permission to override base policy
        // enabled: false
        source: 'Prompt'
      }
      {
        name: 'sexual'
        severityThreshold: 'High' // ['Low', 'Medium', 'High']
        blocking: true // [true, false] TODO: add permission to override base policy
        // enabled: false
        source: 'Completion'
      }
      {
        name: 'violence'
        severityThreshold: 'High' // ['Low', 'Medium', 'High']
        blocking: true // [true, false] TODO: add permission to override base policy
        // enabled: false
        source: 'Prompt'
      }
      {
        name: 'violence'
        severityThreshold: 'High' // ['Low', 'Medium', 'High']
        blocking: true // [true, false] TODO: add permission to override base policy
        // enabled: false
        source: 'Completion'
      }
      {
        name: 'selfharm'
        severityThreshold: 'High' // ['Low', 'Medium', 'High']
        blocking: true // [true, false] TODO: add permission to override base policy
        // enabled: false
        source: 'Prompt'
      }
      {
        name: 'selfharm'
        severityThreshold: 'High' // ['Low', 'Medium', 'High']
        blocking: true // [true, false] TODO: add permission to override base policy
        // enabled: false
        source: 'Completion'
      }
    ]
  }
}

resource llmDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-06-01-preview' = {
  parent: aiServices
  name: addPrefixAndSuffix(llmModelName)
  sku: {
    name: 'Standard'
    capacity: llmModelCapacity
  }
  properties: {
    model: {
      format: llmModelFormat
      name: llmModelName
      version: llmModelVersion
    }
    raiPolicyName: llmNoContentFilter.name
    versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
  }
  dependsOn: [
    llmNoContentFilter
  ]
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

// ********************************************
// OUTPUTS
// ********************************************

output aiServicesName string = aiServices.name
output aiServicesEndpoint string = aiServices.properties.endpoint
output aiFoundryProjectName string = aiFoundryProject.name
output aiFoundryLLMDeploymentName string = llmDeployment.name
output aiFoundryLLMApiVersion string = llmDeployment.apiVersion
