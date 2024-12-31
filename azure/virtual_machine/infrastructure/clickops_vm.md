
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
nc -zv <$VM_IP_ADDRESS> 22
# http port
nc -zv <$VM_IP_ADDRESS> 80
# https port
nc -zv <$VM_IP_ADDRESS> 443
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

## Setup NVIDIA GPU drivers

install modprobe
ref. https://learn.microsoft.com/en-us/azure/virtual-machines/linux/n-series-driver-setup

verify that the system has a CUDA-capable GPU
```bash
lspci | grep -i NVIDIA
```

Install ubuntu-drivers utility:
```bash
sudo apt update && sudo apt install -y ubuntu-drivers-common
```

Install the latest NVIDIA drivers:
```bash
sudo ubuntu-drivers install
```

reboot after installation
```bash
sudo reboot
```

Download and install the CUDA toolkit from NVIDIA:
The example shows the CUDA package path for Ubuntu 24.04 LTS. Replace the path specific to the version you plan to use.
```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
# run the following command twice
sudo apt install -y ./cuda-keyring_1.1-1_all.deb
sudo apt install -y ./cuda-keyring_1.1-1_all.deb
sudo apt update
# the following can take a few minutes
sudo apt -y install cuda-toolkit-12-5
```

reboot after installation
```bash
sudo reboot
```

Verify that the GPU is correctly recognized
```bash
nvidia-smi
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

# Monitor resource utilisation

what is using the GPU memory
```bash
sudo fuser -v /dev/nvidia
```

optionally, kill the process
```bash
sudo kill -9 <$PID>
```

## nvidia-smi
NVidia GPU monitor utilisation
NVIDIA System Management Interface (nvidia-smi)
ref. https://developer.nvidia.com/system-management-interface

```bash
nvidia-smi
```

update the GPU utilisation every 0.1 seconds (creates a log stream)
```bash
nvidia-smi -q -d utilization -l
```

alternatively use watch
```bash
watch -n0.1 nvidia-smi
```

## gpustat
ref. https://github.com/wookayin/gpustat

```bash
#sudo apt install python3
#sudo apt install python3.12-venv
#sudo apt install python3-pip
#python3 -m venv .venv
#.venv/bin/pip install gpustat
sudo apt install gpustat
gpustat --color --show-pid --interval 1
```


## nvtop
ref. https://github.com/Syllo/nvtop

similar to htop (https://htop.dev/)

When the video encoder (ENC) and decoder (DEC) of the GPU are in use, new percentage meters will appear next to the GPU utilization bar. They will disappear automatically after some time of inactivity.

GPU utilization is the percentage of a graphics processing unit's (GPU) processing power that is being used at a given time.

GPU memory is the on-chip memory in a graphics processing unit (GPU) that stores and manages data for graphics and video processing. It's also known as video random access memory (VRAM)

GPU utilisation is referring to load on the actual graphics processor, not how much VRAM is being used. A completely full VRAM would hurt performance because the GPU would have to swap data in and out of system memory, but it wouldn't necessarily increase GPU utilisation.

Install on Ubuntu
```bash
sudo apt install nvtop
```

Manual page
```bash
man nvtop
nvtop --help
```

Run
```bash
nvtop
```

## Azure
ref. https://techcommunity.microsoft.com/t5/azure-high-performance-computing/comprehensive-nvidia-gpu-monitoring-for-azure-n-series-vms-using/ba-p/4257402#:~:text=To%20visualize%20NVIDIA%20GPU%20usage,to%20view%20NVIDIA%20GPU%20utilization.

ERROR: Not Found IP
replicated with steps from https://docs.influxdata.com/telegraf/v1/install/

## BTOP
ref. https://github.com/aristocratos/btop

## Glances
(not tested)
ref. https://glances.readthedocs.io/en/latest/install.html

Install
```bash
pip install python-dev
pip install glances
```

# Terminate your resource

Terminate all resources that you have created during this session.
