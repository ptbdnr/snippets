install modprobe
ref. https://learn.microsoft.com/en-us/azure/virtual-machines/linux/n-series-driver-setup

verify that the system has a CUDA-capable GPU
```bash
lspci | grep -i NVIDIA
```

# Install

## Install NVIDIA GPU drivers

```bash
sudo apt update && sudo apt install -y ubuntu-drivers-common
sudo ubuntu-drivers install
# reboot after installation
sudo reboot
```

## Install CUDA toolkit

Download and install the CUDA toolkit from NVIDIA:
The example shows the CUDA package path for Ubuntu 24.04 LTS. Replace the path specific to the version you plan to use.

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
sudo apt update
# run the following command twice
sudo apt install -y ./cuda-keyring_1.1-1_all.deb
sudo apt install -y ./cuda-keyring_1.1-1_all.deb
sudo apt update
# the following can take a few minutes
sudo apt -y install cuda-toolkit-12-5
# reboot after installation
sudo reboot
```

Verify that the GPU is correctly recognized
NVIDIA System Management Interface (nvidia-smi)
ref. https://developer.nvidia.com/system-management-interface

```bash
nvidia-smi
```

# Monitor resource utilization

```bash
# what is using the GPU memory
sudo fuser -v /dev/nvidia
# optionally, kill the process
sudo kill -9 <$PID>
sudo apt install gpustat
gpustat --color --show-pid --interval 1
sudo apt install nvtop
nvtop
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