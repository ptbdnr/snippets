// Parameters
// @description('Name of the resource group where all resources will be created.')
// param resourceGroupName string

@description('Location for all resources.')
param location string = resourceGroup().location

@description('Name of the virtual network.')
param vnetName string = 'vnet-${uniqueString(resourceGroup().id)}'

@description('The name of the virtual network subnet to be associated with the Azure Function app.')
param functionSubnetName string = 'snet-func'

@description('Name of the virtual network subnet used for allocating IP addresses for private endpoints.')
param privateEndpointSubnetName string = 'snet-pe'

@description('Name of the storage account.')
param storageAccountName string = 'st'

@description('Name of the private endpoint.')
param privateEndpointToStorageName string

@description('Name of the private DNS zone.')
param privateDnsZoneName string

@description('Name of the app service plan.')
param functionAppServicePlanName string = 'func-plan-${uniqueString(resourceGroup().id)}'

@description('Specifies the OS used for the Azure Function hosting plan.')
@allowed([
  'Windows'
  'Linux'
])
param functionPlanOS string = 'Linux'

@description('Name of the backend storage account used by the function app.')
param functionStorageAccountName string = 'funcst${uniqueString(resourceGroup().id)}'

@description('Name of the function app.')
param functionAppName string = 'func-${uniqueString(resourceGroup().id)}'

@description('Only required for Linux app to represent runtime stack in the format of \'runtime|runtimeVersion\'. For example: \'python|3.9\'')
param linuxFxVersion string = 'python|3.11'

var isReserved = ((functionPlanOS == 'Linux') ? true : false)
var functionContentShareName = toLower('function-content-share')
var functionWorkerRuntime = 'python'
// var privateFunctionAppDnsZoneName = 'privatelink.azurewebsites.net'
// var privateEndpointFunctionAppName = '${functionAppName}-private-endpoint'

// // Create Resource Group
// targetScope = 'subscription'
// resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
//   name: resourceGroupName
//   location: location
// }

// Create Virtual Network with Subnet
targetScope = 'resourceGroup'
resource virtualNetwork 'Microsoft.Network/virtualNetworks@2023-11-01' = {
  name: vnetName
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'  // The IP adddress space used for the virtual network.
      ]
    }
    subnets: [
      {
        name: privateEndpointSubnetName
        properties: {
          privateEndpointNetworkPolicies: 'Disabled'
          privateLinkServiceNetworkPolicies: 'Enabled'
          addressPrefix: '10.0.0.0/24' // The IP address space used for the subnet.
        }
      }
      {
        name: functionSubnetName
        properties: {
          privateEndpointNetworkPolicies: 'Enabled'
          privateLinkServiceNetworkPolicies: 'Enabled'
          delegations: [
            {
              name: 'webapp'
              properties: {
                serviceName: 'Microsoft.Web/serverFarms'
              }
            }
          ]
          addressPrefix: '10.0.1.0/24' // 'The IP address space used for the Azure Function integration subnet.'
        }
      }
    ]
  }
}

// Create Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    // allowBlobPublicAccess: false
    publicNetworkAccess: 'Disabled'
  }
}

// Create Private Endpoint for Storage Account
var storage_account_id = storageAccount.id
resource privateEndpointToStorage 'Microsoft.Network/privateEndpoints@2022-05-01' = {
  name: privateEndpointToStorageName
  location: location
  properties: {
    subnet: {
      id: resourceId('Microsoft.Network/virtualNetworks/subnets', vnetName, privateEndpointSubnetName)
    }
    customNetworkInterfaceName: '${privateEndpointToStorageName}-nic'
    privateLinkServiceConnections: [
      {
        name: 'storageAccountPrivateLinkConnection'
        properties: {
          privateLinkServiceId: storage_account_id
          groupIds: [
            'blob'
          ]
        }
      }
    ]
  }
  dependsOn: [
    virtualNetwork
  ]
}

// Create Private DNS Zone
resource privateDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
  name: privateDnsZoneName
  location: 'global'
}

// Link Private DNS Zone to Virtual Network
resource privateDnsZoneVnetLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
  parent: privateDnsZone
  name: '${privateDnsZoneName}-link'
  location: 'global'
  properties: {
    registrationEnabled: false
    virtualNetwork: {
      id: virtualNetwork.id
    }
  }
}

// Create DNS A Record in Private DNS Zone
// var pep_ipv4 = privateEndpointToStorage.properties.networkInterfaces[0].properties.ipConfigurations[0].properties.privateIPAddress
// resource dnsARecord 'Microsoft.Network/privateDnsZones/A@2020-06-01' = {
//   name: '${storageAccountName}.${privateDnsZoneName}'
//   parent: privateDnsZone
//   properties: {
//     ttl: 3600
//     aRecords: [
//       {
//         ipv4Address: pep_ipv4
//       }
//     ]
//   }
// }

resource privateEndpointStoragePrivateDnsZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2023-11-01' = {
  parent: privateEndpointToStorage
  name: '${privateEndpointToStorageName}-PrivateDnsZoneGroup'
  properties: {
    privateDnsZoneConfigs: [
      {
        name: 'config'
        properties: {
          privateDnsZoneId: privateDnsZone.id
        }
      }
    ]
  }
}

// Create App Service Plan, recommended for production workloads
resource functionAppServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: functionAppServicePlanName
  location: location
  sku: {
    name: 'B1' 
    tier: 'Basic'
  }
  properties: {
    reserved: isReserved
  }
}

// storage account for function app
resource functionStorageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: functionStorageAccountName
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  // properties: {
  //   publicNetworkAccess: 'Disabled'
  //   allowBlobPublicAccess: false
  //   networkAcls: {
  //     bypass: 'None'
  //     defaultAction: 'Deny'
  //   }
  // }
}

// file share for Function App, required for deployment
resource fileService 'Microsoft.Storage/storageAccounts/fileServices/shares@2023-05-01' = {
  name: '${functionStorageAccountName}/default/${functionContentShareName}'
  dependsOn: [
    storageAccount
  ]
}

// // Create Function App
resource functionApp 'Microsoft.Web/sites@2022-03-01' = {
  name: functionAppName
  location: location
  kind: (isReserved ? 'functionapp,linux' : 'functionapp')
  properties: {
    reserved: isReserved
    serverFarmId: functionAppServicePlan.id
    siteConfig: {
      linuxFxVersion: (isReserved ? linuxFxVersion : null)
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${functionStorageAccountName};AccountKey=${functionStorageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net'
        }
        // {
        //   name: 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING'
        //   value: 'DefaultEndpointsProtocol=https;AccountName=${functionStorageAccountName};AccountKey=${functionStorageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net'
        // }
        // {
        //   name: 'WEBSITE_CONTENTSHARE'
        //   value: functionContentShareName
        // }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: functionWorkerRuntime
        }
        // {
        //   name: 'WEBSITE_NODE_DEFAULT_VERSION'
        //   value: '~14'
        // }
        // {
        //   name: 'WEBSITE_VNET_ROUTE_ALL'
        //   value: '1'
        // }
        // {
        //   name: 'WEBSITE_CONTENTOVERVNET'
        //   value: '1'
        // }
      ]
    }
  }  
  dependsOn: [
    functionAppServicePlan  
    functionStorageAccount  // necessary for AzureWebJobsStorage
    privateEndpointToStorage
    privateDnsZone
    privateDnsZoneVnetLink
    // dnsARecord
  ]
}

// // Enable VNet Integration for Function App
// resource networkConfig 'Microsoft.Web/sites/networkConfig@2022-09-01' = {
//   parent: functionApp
//   name: 'virtualNetwork'
//   properties: {
//     subnetResourceId: resourceId('Microsoft.Network/virtualNetworks/subnets', vnetName, functionSubnetName)
//     swiftSupported: true
//   }
//   dependsOn: [
//     virtualNetwork
//   ]
// }

// resource privateFunctionAppDnsZone 'Microsoft.Network/privateDnsZones@2020-06-01' = {
//   name: privateFunctionAppDnsZoneName
//   location: 'global'
// }

// resource privateDnsZoneLink 'Microsoft.Network/privateDnsZones/virtualNetworkLinks@2020-06-01' = {
//   parent: privateFunctionAppDnsZone
//   name: '${privateFunctionAppDnsZoneName}-link'
//   location: 'global'
//   properties: {
//     registrationEnabled: false
//     virtualNetwork: {
//       id: virtualNetwork.id
//     }
//   }
// }

// resource privateEndpoint 'Microsoft.Network/privateEndpoints@2022-05-01' = {
//   name: privateEndpointFunctionAppName
//   location: location
//   properties: {
//     subnet: {
//       id: resourceId('Microsoft.Network/virtualNetworks/subnets', vnetName, privateEndpointSubnetName)
//     }
//     privateLinkServiceConnections: [
//       {
//         name: 'MyFunctionAppPrivateLinkConnection'
//         properties: {
//           privateLinkServiceId: functionApp.id
//           groupIds: [
//             'sites'
//           ]
//         }
//       }
//     ]
//   }
//   dependsOn: [
//     virtualNetwork
//   ]
// }

// resource privateDnsZoneGroup 'Microsoft.Network/privateEndpoints/privateDnsZoneGroups@2022-05-01' = {
//   parent: privateEndpoint
//   name: 'funcPrivateDnsZoneGroup'
//   properties: {
//     privateDnsZoneConfigs: [
//       {
//         name: 'config'
//         properties: {
//           privateDnsZoneId: privateFunctionAppDnsZone.id
//         }
//       }
//     ]
//   }
// }
