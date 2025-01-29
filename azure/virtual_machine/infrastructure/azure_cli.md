# IaaC with Azure CLI

## Requirements

* Azure subscription
* Azure CLI: to sing-in to the Azure account

```shell
# Azure CLI expected version: 2.61 or higher
az --version
```

## Sign in

```bash
az login
```

Set variables

```bash
RESOURGE_GROUP_NAME="*************"
VM_NAME="************"
LOCATION="swedencentral"
IMAGE="Ubuntu2404"
SIZE="Standard_NC12s_v3"
ADMIN_USERNAME="azureuser"
SSH_KEY_PATH="~/.ssh/id_rsa.pub"
```

## Create Azure resources

1. Create resource group

```bash
az group create 
    --name $RESOURGE_GROUP_NAME \ 
    --location $LOCATION \ 
    --tags Owner=$USERNAME
```

2. Create virtual machine

OS (or Data) disk size: for AI models select 500GB or more to store model manifests

```bash
az vm create 
    --resource-group $RESOURGE_GROUP_NAME
    --name $VM_NAME
    --image $IMAGE
    --size $SIZE
    --admin-username $ADMIN_USERNAME
    --generate-ssh-keys
    --public-ip-sku Standard
    --custom-data cloud-init.txt
    --os-disk-sizes-gb 512
```

3. Open ports

```bash
az vm open-port --port 80 --priority 1001 --resource-group $RESOURGE_GROUP_NAME --name $VM_NAME
az vm open-port --port 443 --priority 1002 --resource-group $RESOURGE_GROUP_NAME --name $VM_NAME
az vm open-port --port 22 --priority 1003 --resource-group $RESOURGE_GROUP_NAME --name $VM_NAME
```

Get public IP address

```bash
VM_IP_ADDRESS=$(az vm show --show-details --resource-group $RESOURGE_GROUP_NAME --name $VM_NAME --query publicIps -o tsv)
echo "VM IP Address: $VM_IP_ADDRESS"
```

Test connection to the VM

```bash
# ssh port
nc -zv $VM_IP_ADDRESS 22
# http port
nc -zv $VM_IP_ADDRESS 80
# https port
nc -zv $VM_IP_ADDRESS 443
```

## Log in 

Log in via SSH

```bash
ssh $ADMIN_USERNAME@$VM_IP_ADDRESS
```

## Install software

Install and launch Jupyter Notebook

```bash
curl -L https://tljh.jupyter.org/bootstrap.py | sudo python3 - --admin $ADMIN_USERNAME
```

Programmatic access

```bash
az group list
az vm list > az_vm_list.json && nano az_vm_list.json
az storage account list > az_sa_list.json && nano az_sa_list.json
```

## Terminate resources

```bash
az group delete --name $RESOURCE_GROUP --yes --no-wait
```