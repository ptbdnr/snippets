
# Sign in
In a browser navigate to http://portal.azure.com/
Click on your profile picture/avatar on the top right corner
Click on Switch directory
Switch to the directory (if it is not already the Current)
* name: *********
* domain: *********.onmicrosoft.com
* ID: *****************
Search for the Subscriptions service
Verify that subscription named `********` is listed

# Launch an Virtual Computer

In Azure Portal, click on the search bar.
Search and select the service: `Virtual machines`.
Click on `+ Create`, select `Azure Virtual machine`, and configure as follows:
* Subscription: leave it on default
* Resource group: *************
* Virtual machine name: `************`
* Region: (Europe) UK South
* Image: leave it on default, or select OS Linux (ubuntu 24.04)
* Size: leave it on default for generic, for GPU use NC or ND family
  for example: Standard NC 12 v3 (12 cores, 224B RAM, 2x Tesla V100 16GB vRAM)
* Authentication type: SSH public key (less secure option is to use username and password)
* Username: leave it on default (azureuser)
* Key pair name: leave it on default
* Public inbound ports: Allow HTTP (80), HTTPS (443), SSH(22)
* OS disk size: for AI models select 500GB or more to store model manifests
Click on Tags
* Name: `owner`
* Value: `[YOUR NAME]`
Click `Review + create`
Click `Create`
Once the pop-up window appears click on `Download private key and create resource`

# Connect to the Virtual Computer

Once successfully initiated the launch,
In Azure Portal, click on the search bar.
Search and select the service: `Virtual machines`.
From the list, find your new virtual instance, click on the instance name.
Save the Public IP Address (e.g. IP address: 135.225.130.47)

Test connection to the VM from your local computer
```bash
# ssh port
nc -zv $VM_IP_ADDRESS 22
# http port
nc -zv $VM_IP_ADDRESS 80
# https port
nc -zv $VM_IP_ADDRESS 443
```

# Log in

## Log in via SSH with a password
```bash
ssh <$USERNAME>@<$VM_IP_ADDRESS>
```

## Log in via SSH with a private key
Click on Connect, select `SSH` (on Windows it is `Native SSH`)

Follow the instructions on Azure: ensure you have access to the .pem file, provide the path to it, and invoke the generated ssh command.

# Use the Virtual Computer

Once logged in to the VM, verify the IP address of the machine
```bash
curl https://ifconfig.me
```

## Install and Launch Jupyter Notebook

with a single command
```bash
curl -L https://tljh.jupyter.org/bootstrap.py \
  | sudo python3 - \
    --admin azureuser
```

OR do it step-by-step (+ add port redirect)
```bash
sudo apt-get update
python3 --version
sudo apt-get install python3-pip -y
pip --version
export PATH="/home/azureuser/.local/bin:$PATH"
pip install markupsafe==2.0.1
pip install notebook
jupyter notebook --ip=* --allow_origin='*' --no-browser --allow-root
```

Virtual Computer as a remote server

In Azure Portal, click on the search bar.
Search and select the service: `Virtual machines`.
From the list, find your new virtual instance, click on the instance name.
In the navigation menu find and select 'Overview'.
Search for Public IP address and open a new browser tab:
`http://[PUBLIC_IP_ADDRESS]/`
usename: azureuser
password: azureuser

# Programmatic access

This section uses your local computer.

## Get your credentials

install Azure CLI: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli
```bash
az --version
az login
```

Troubleshooting
1. Error: Certificate verification failed. This typically happens when using Azure CLI behind a proxy ... Try to get and configure the certificate for your proxy

## Store your credentials

The credentials are stored automatically with `az login`
under the folder `~/.azure`

## Use the programmatic access

Try

on Unix
```bash
az group list
az vm list > az_vm_list.json && nano az_vm_list.json
az storage account list > az_sa_list.json && nano az_sa_list.json
```

on Windows
```batch
az group list
az vm list > az_vm_list.json
az storage account list > az_sa_list.json
```

# Terminate your resource

Terminate all resources that you have created during this session.
