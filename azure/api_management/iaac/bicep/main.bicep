targetScope = 'resourceGroup'

@description('Location for all resources')
param rLocation string

@description('OpenAPI specifications')
param openapi string

func addPrefixAndSuffix(name string) string => 'foo-${name}-bar'

// API Management
resource apiMgmt 'Microsoft.ApiManagement/service@2024-05-01' = {
  name: addPrefixAndSuffix('apim')
  location: rLocation
  sku: {
    name: 'Developer'
    capacity: 1
  }
  properties: {
    publisherName: 'Kainos'
    publisherEmail: 'peter.bodnar@kainos.com'
  }
}

resource apimSubscription 'Microsoft.ApiManagement/service/subscriptions@2024-06-01-preview' = {
  parent: apiMgmt
  name: addPrefixAndSuffix('apim-subscription')
  properties: {
    allowTracing: true
    displayName: 'all_apis_subscription'
    scope: '/apis'
  }
}

resource apimVersionSet 'Microsoft.ApiManagement/service/apiVersionSets@2024-05-01' = {
  parent: apiMgmt
  name: addPrefixAndSuffix('api-version-set')
  properties: {
    displayName: 'Foo VS'
    description: 'Version set for Foo API'
    versioningScheme: 'Header'
    versionHeaderName: 'version'
  }  
}
output apimVersionSet string = apimVersionSet.id

resource apimapi 'Microsoft.ApiManagement/service/apis@2024-05-01' = {
  parent: apiMgmt
  name: addPrefixAndSuffix('api')
  properties: {
    type: 'http'
    displayName: 'Foo'
    description: 'API for Foo'
    path: 'foo'
    apiVersion: '1.0'
    subscriptionRequired: true
    format: 'openapi+json'
    value: openapi
    apiVersionSetId: apimVersionSet.id
    serviceUrl: 'https://example.com'
  }
}
output apimapiId string = apimapi.id
