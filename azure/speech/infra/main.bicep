targetScope = 'resourceGroup'

@description('Location for all resources')
param rLocation string

var rNamePrefix = 'foo'
var rNameSuffix = 'bar'

func addPrefixAndSuffix(name string) string => '${rNamePrefix}-${name}-${rNameSuffix}'


resource speechServices 'Microsoft.CognitiveServices/accounts@2021-04-30' = {
  name: addPrefixAndSuffix('speechservices')
  location: rLocation
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: 'S0'
  }
  kind: 'SpeechServices'
  properties: {
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    capabilities: [
      {
        name: 'CommitmentPlan'
      }
      {
        name: 'VirtualNetworks'
      }
      {
        name: 'CustomerManagedKey'
      }
      {
        name: 'Container'
        value: 'SpeechServices.CustomSpeechToText,SpeechServices.NeuralTextToSpeechOnPrem,SpeechServices.DPP,SpeechServices.SpeechToText,SpeechServices.ctsdiarizer,SpeechServices.diarization'
      }
    ]
  }
  tags: {}
}
