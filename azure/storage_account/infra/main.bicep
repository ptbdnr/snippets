targetScope = 'resourceGroup'

// ********************************************
// PARAMETERS
// ********************************************

@description('Project Name')
param projectName string

@description('Environment')
@allowed(['dev', 'tst', 'prd'])
param environment string

@description('Location for all resources')
param location string

@description('VNet ID')
param vnetId string

@description('Subnet ID')
param subnetId string

@description('Function App Identity Principal ID')
param identityId string

@description('Retention days for data in the Storage Account')
param retentionDays int

// ********************************************
// VARIABLES
// ********************************************

var rgProjectName = projectName
var rgNameSuffix = '${environment}'

func addPrefixAndSuffix(name string) string => '${name}-${rgProjectName}-${rgNameSuffix}'
func nohyphen(input string) string => toLower(replace(input, '-', ''))

// Define the IDs of the roles we need to assign to our managed identities.
// https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles
var storageBlobDataContributorRoleId = 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
var storageTableDataContributorRoleId = '0a9a7e1f-b9d0-4cc4-a60d-0319b160aaa3'

// ********************************************
// DATA STORE
// ********************************************

// Storage Account for Blob and Table Store
resource sa 'Microsoft.Storage/storageAccounts@2025-01-01' = {
  name: nohyphen(addPrefixAndSuffix('sa'))
  location: location
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
  properties: {
    accessTier: 'Hot'
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
    publicNetworkAccess: environment == 'prod' ? 'Disabled' : 'Enabled'
    allowBlobPublicAccess: environment == 'prod' ? true : false
    networkAcls: {
      defaultAction: environment == 'prod' ? 'Deny' : 'Allow'
      bypass: 'AzureServices'
      virtualNetworkRules: [
        {
          id: subnetId
          action: 'Allow'
        }
      ]
    }    
  }
}

// Blob containers for files
resource blobs 'Microsoft.Storage/storageAccounts/blobServices@2025-01-01' = {
  name: 'default'
  parent: sa
}

resource fileContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2025-01-01' = {
  name: 'files'
  parent: blobs
  properties: {
    publicAccess: 'None'
  }
}

// Tables for lookups
resource tables 'Microsoft.Storage/storageAccounts/tableServices@2025-01-01' = {
  name: 'default'
  parent: sa
}

resource filesTable 'Microsoft.Storage/storageAccounts/tableServices/tables@2025-01-01' = {
  name: 'files'
  parent: tables
}

// ********************************************
// POLICY
// ********************************************

// Enforce X day retention policy for blob soft delete
resource saMgmtPolicy 'Microsoft.Storage/storageAccounts/managementPolicies@2025-01-01' = {
  name: 'default'
  parent: sa
  properties: {
    policy: {
      rules: [
        {
          name: addPrefixAndSuffix('blob-retention-Xdays')
          enabled: true
          type: 'Lifecycle'
          definition: {
            actions: {
              baseBlob: {
                delete: {
                  daysAfterCreationGreaterThan: retentionDays
                }
              }
              snapshot: {
                delete: {
                  daysAfterCreationGreaterThan: retentionDays
                }
              }
              version: {
                delete: {
                  daysAfterCreationGreaterThan: retentionDays
                }
              }
            }
            filters: {
              blobTypes: ['blockBlob']
              prefixMatch: []
            }
          }
        }
        {
          name: addPrefixAndSuffix('table-retention-Xdays')
          enabled: true
          type: 'Lifecycle'
          definition: {
            actions: {
              baseBlob: {
                delete: {
                  daysAfterCreationGreaterThan: retentionDays
                }
              }
            }
            filters: {
              blobTypes: ['blockBlob']
              prefixMatch: []
            }
          }
        }        
      ]
    }
  }
}

// ********************************************
// ROLE ASSIGNMENTS
// ********************************************

// Grant the Identity a read+write permission on Storage Blob
resource roleAssignmentBlob 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().id, resourceGroup().id, identityId, sa.id, storageBlobDataContributorRoleId)
  scope: sa
  properties: {
    principalType: 'ServicePrincipal' // ['User', 'ServicePrincipal']
    principalId: identityId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', storageBlobDataContributorRoleId)
  }
}

// Grant the Identity a read+write permission on Storage Table
resource roleAssignmentTable 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().id, resourceGroup().id, identityId, sa.id, storageTableDataContributorRoleId)
  scope: sa // saTable
  properties: {
    principalType: 'ServicePrincipal' // ['User', 'ServicePrincipal']
    principalId: identityId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', storageTableDataContributorRoleId)
  }
}

// ********************************************
// Private DNS Zones within the VNet
// ********************************************

resource pDnsZoneStorage 'Microsoft.Network/privateDnsZones@2024-06-01' = {
  name: 'privatelink.blob.${az.environment().suffixes.storage}'
  location: 'global'
}

resource vnetLinkStorage 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2024-06-01' = {
  name: '${pDnsZoneStorage.name}-link'
  parent: pDnsZoneStorage
  location: 'global'
  properties: {
    registrationEnabled: false  // private endpoint handles DNS registration automatically
    virtualNetwork: { id: vnetId }
  }
}

// ********************************************
// Private Endpoints within the Subnet
// ********************************************

// Private Endpoint for Azure Storage
resource peStorage 'Microsoft.Network/privateEndpoints@2024-05-01' = {
  name: addPrefixAndSuffix('pe-storage')
  location: location
  properties: {
    subnet: {
      id: subnetId
    }
    privateLinkServiceConnections: [
      {
        name: 'pe-connection-sa'
        properties: {
          privateLinkServiceId: sa.id
          groupIds: [
            'blob'
          ]
        }
      }
    ]
  }
  dependsOn: [ sa ]
}

// ********************************************
// Connect Private Endpoints to Private DNS Zones
// ********************************************

resource peDnsGroupStorage 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2024-07-01' = {
  parent: peStorage
  name: 'default'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'config-sa'
        properties: {
          privateDnsZoneId: pDnsZoneStorage.id
        }
      }
    ]
  }
  dependsOn: [
    peStorage
    pDnsZoneStorage
  ]
}

// ********************************************
// OUTPUTS
// ********************************************

output saBlobId string = sa.id
output saBlobName string = sa.name
output filesContainerId string = filesContainer.id
output filesContainerName string = filesContainer.name

output saTableId string = sa.id
output saTableName string = sa.name
output filesTableId string = filesTable.id
output filesTableName string = filesTable.name
