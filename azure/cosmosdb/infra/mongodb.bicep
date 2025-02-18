@description('Location for all resources')
param rLocation string

var rNamePrefix = 'foo'
var rNameSuffix = 'buz'

func addPrefixAndSuffix(name string) string => '${main.rgNamePrefix}-${name}-${rNameSuffix}'


// Cosmos DB - MongoDB
resource nosqlAccount 'Microsoft.DocumentDB/databaseAccounts@2022-05-15' = {
  name: addPrefixAndSuffix('nosql')
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

resource nosqlKnowledgeDatabase 'Microsoft.DocumentDB/databaseAccounts/mongodbDatabases@2022-05-15' = {
  parent: nosqlAccount
  name: 'knowledge'
  properties: {
    resource: {
      id: 'knowledge'
    }
    options: {
      throughput: 400
    }
  }
}

var nosqlKnowledgeCollectionCustomersName = 'customers'
resource nosqlCustomerCollectionCustomers 'Microsoft.DocumentDb/databaseAccounts/mongodbDatabases/collections@2022-05-15' = {
  parent: nosqlKnowledgeDatabase
  name: nosqlKnowledgeCollectionCustomersName
  properties: {
    resource: {
      id: nosqlKnowledgeCollectionCustomersName
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

var nosqlKnowledgeCollectionAppointmentsName = 'appointments'
resource nosqlCustomerCollectionAppointments 'Microsoft.DocumentDb/databaseAccounts/mongodbDatabases/collections@2022-05-15' = {
  parent: nosqlKnowledgeDatabase
  name: nosqlKnowledgeCollectionAppointmentsName
  properties: {
    resource: {
      id: nosqlKnowledgeCollectionAppointmentsName
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
      ]
    }
  }
}
