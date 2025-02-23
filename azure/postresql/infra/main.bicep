var rNamePrefix = 'foo'
var rNameSuffix = 'bar'

@description('Location for all resources')
param rLocation string

@description('PostgreSQL credentials')
param postgresAdminUser string
@secure()
param postgresAdminPassword string

func addPrefixAndSuffix(name string) string => '${main.rgNamePrefix}-${name}-${rNameSuffix}'

// PostgreSQL
resource postgres 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
  name: addPrefixAndSuffix('pg')
  location: rLocation
  properties: {
    version: '14'
    administratorLogin: postgresAdminUser
    administratorLoginPassword: postgresAdminPassword
    storage: {
      storageSizeGB: 32
    }
    backup: {
      backupRetentionDays: 7
    }
  }
  sku: {
    name: 'Standard_E4ds_v4'
    tier: 'MemoryOptimized'
  }
}
