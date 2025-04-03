using './main.bicep'

@description('Location for all resources')
param rLocation = 'uswest3'

@description('The OpenAPI document to be used for the API Management service')
param openapi = loadTextContent('./openapi.json')
