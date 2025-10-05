targetScope = 'resourceGroup'

// ********************************************
// PARAMETERS
// ********************************************

@description('Location for all resources')
param rLocation string

@description('Identity ID')
param identityId string

// ********************************************
// VARIABLES
// ********************************************

var rNamePrefix = 'foo'
var rNameSuffix = 'buz'

func addPrefixAndSuffix(name string) string => '${main.rgNamePrefix}-${name}-${rNameSuffix}'

// ********************************************
// NEW RESOURCES
// ********************************************

// Cosmos DB - MongoDB
resource mongodb 'Microsoft.DocumentDB/databaseAccounts@2022-05-15' = {
  name: addPrefixAndSuffix('mongodb')
  location: rLocation
  kind: 'MongoDB'
  properties: {
    consistencyPolicy: {
      defaultConsistencyLevel: 'Eventual'
    }
    locations: [{
      locationName: rLocation
      failoverPriority: 0
      isZoneRedundant: false
    }]
    databaseAccountOfferType: 'Standard'
    enableAutomaticFailover: true
    apiProperties: {
      serverVersion: '4.2'
    }
    capabilities: [
      {
        name: 'DisableRateLimitingResponses'
      }
    ]
  }
}

resource mongodbDatabase 'Microsoft.DocumentDB/databaseAccounts/mongodbDatabases@2022-05-15' = {
  parent: mongodb
  name: 'mongodbdb'
  properties: {
    resource: {
      id: 'mongodbdb'
    }
    options: {
      throughput: 400
    }
  }
}

resource mongodbCollection 'Microsoft.DocumentDb/databaseAccounts/mongodbDatabases/collections@2022-05-15' = {
  parent: mongodbDatabase
  name: 'mongodbcontainer1'
  properties: {
    resource: {
      id: 'mongodbcontainer1'
      shardKey: {
        _shard_key: 'Hash'
      }
      indexes: [
        {
          key: {
            keys: [
              '_id'
              '_shard_key'
            ]
          }
        }
        {
          key: {
            keys: [
              '$**'
            ]
          }
        }
      ]
    }
  }
}

// ********************************************
// ROLES
// ********************************************

resource cosmosDBSQLRole 'Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions@2024-11-15' = {
  name: guid(subscription().id, resourceGroup().id, mongodb.id, 'cosmosDBSQLRole')
  parent: mongodb
  properties: {
    roleName: 'Azure Mongo DB SQL Role'
    type: 'CustomRole'
    permissions: [
      {
        dataActions: [
          'Microsoft.DocumentDB/databaseAccounts/readMetadata'
          'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*'
          'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*'
        ]
      }
    ]
    assignableScopes: [
      mongodb.id
    ]
  }
}

// ********************************************
// ROLE ASSIGNMENTS
// ********************************************

// Grant the Itentity a read+write permission on the CosmosDB (formerly known as DocumentDB)
resource roleAssignmentSQL 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2024-11-15' = {
  name: guid(subscription().id, functionAppIdentityPrincipalId, mongodb.id, 'cosmosDBSQLRole')
  parent: mongodb
  properties: {
    principalId: IdentityId
    scope: mongodb.id
    roleDefinitionId: cosmosDBSQLRole.id
  }
}

// ********************************************
// OUTPUTS
// ********************************************

output mongodblId string = mongodb.id
output mongodbName string = mongodb.name
output mongodbUrl string = mongodb.properties.documentEndpoint
output mongodbDatabaseId string = mongodbDatabase.id
output mongodbContainerId string = mongodbCollection.id
