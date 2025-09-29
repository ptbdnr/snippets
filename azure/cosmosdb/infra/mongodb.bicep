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

// Cosmos DB - NoSQL

// Cosmos DB for database
resource nosql 'Microsoft.DocumentDB/databaseAccounts@2025-05-01-preview' = {
  name: addPrefixAndSuffix('nosql')
  location: rLocation
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: rLocation
        failoverPriority: 0
      }
    ]
    networkAclBypass: 'None'
    publicNetworkAccess: 'Enabled' // TODO: delete line
    isVirtualNetworkFilterEnabled: false // TODO: change to true, and use virtualNetworkRules
    // virtualNetworkRules: [
    //   {
    //     id: subnetId
    //     ignoreMissingVNetServiceEndpoint: false
    //   }
    // ]
  }
}

resource nosqlDatabase 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2025-05-01-preview' = {
  parent: nosql
  name: 'nosqldb'
  properties: {
    resource: {
      id: 'nosqldb'
    }
  }
}

resource nosqlContainer 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2025-05-01-preview' = {
  parent: nosqlDatabase
  name: 'nosqlcontainer'
  properties: {
    resource: {
      id: 'nosqlcontainer'
      partitionKey: {
        paths: ['/pkey']
        kind: 'Hash'
      }
    }
  }
}

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
  name: guid(subscription().id, resourceGroup().id, nosqlAccount.id, 'cosmosDBSQLRole')
  parent: nosqlAccount
  properties: {
    roleName: 'Azure Cosmos DB SQL Role'
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
      nosqlAccount.id
    ]
  }
}

// ********************************************
// ROLE ASSIGNMENTS
// ********************************************

// Grant the Itentity a read+write permission on the CosmosDB (formerly known as DocumentDB)
resource roleAssignmentSQL 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2024-11-15' = {
  name: guid(subscription().id, functionAppIdentityPrincipalId, nosqlAccount.id, 'cosmosDBSQLRole')
  parent: nosqlAccount
  properties: {
    principalId: IdentityId
    scope: nosqlAccount.id
    roleDefinitionId: cosmosDBSQLRole.id
  }
}

// ********************************************
// OUTPUTS
// ********************************************

output nosqlId string = nosql.id
output nosqlName string = nosql.name
output nosqlUrl string = nosql.properties.documentEndpoint
output nosqlDatabaseId string = nosqlDatabase.id
output nosqlContainerId string = nosqlCollection.id
