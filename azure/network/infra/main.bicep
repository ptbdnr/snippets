targetScope = 'resourceGroup'

@description('Location for all resources')
param rLocation string

@description('Stage')
param stage string

@description('PostgreSQL credentials')
param postgresAdminUser string
@secure()
param postgresAdminPassword string

var rNamePrefix = 'foo'
var rNameSuffix = 'bar'

func addPrefixAndSuffix(name string) string => '${main.rgNamePrefix}-${name}-${rNameSuffix}'

// Data NSG
resource nsgData 'Microsoft.Network/networkSecurityGroups@2022-07-01' = {
  name: addPrefixAndSuffix('nsg')
  location: rLocation
  properties: {}
}

// Data VNet
resource vnetData 'Microsoft.Network/virtualNetworks@2022-07-01' = {
  name: addPrefixAndSuffix('vnet')
  location: rLocation
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
    subnets: [
      {
        name: 'aiconfig'
        properties: {
          addressPrefix: '10.0.0.0/24'
          networkSecurityGroup: {
            id: nsgData.id
          }
        }
      }
      {
        name: 'example'
        properties: {
          addressPrefix: '10.0.1.0/24'
          networkSecurityGroup: {
            id: nsgData.id
          }
        }
      }
    ]
  }
}
