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

// API for Function App integration (legacy approach)
resource functionApi 'Microsoft.ApiManagement/service/apis@2021-12-01-preview' = {
  parent: apiMgmt
  name: addPrefixAndSuffix('func-api')
  properties: {
    displayName: 'Function App API'
    path: 'functions'
    protocols: [
      'https'
    ]
    // Connects API Management to the Function App by using its hostname as the backend URL
    serviceUrl: 'https://example.com'
  }
}

// GET Operation
resource functionApiGet 'Microsoft.ApiManagement/service/apis/operations@2021-12-01-preview' = {
  name: addPrefixAndSuffix('func-api-get')
  parent: functionApi
  properties: {
    displayName: 'Function GET Operation'
    method: 'GET'
    urlTemplate: '/get'
    responses: [
      {
        statusCode: 200
        description: 'Success'
      }
    ]
  }
}

// POST Operation
resource functionApiPost 'Microsoft.ApiManagement/service/apis/operations@2021-12-01-preview' = {
  name: addPrefixAndSuffix('func-api-post')
  parent: functionApi
  properties: {
    displayName: 'Function POST Operation'
    method: 'POST'
    urlTemplate: '/post'
    request: {
      // Optional: Define request details as needed
      queryParameters: []
      headers: []
      representations: []
    }
    responses: [
      {
        statusCode: 200
        description: 'Success'
      }
    ]
  }
}
