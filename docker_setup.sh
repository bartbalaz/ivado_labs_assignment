#!/bin/bash

# Install basic pre-requisites
apt update
apt -y install wget

# Install Nvidia components for GPU access
# See https://developer.nvidia.com/cuda-downloads for details
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.2.2/local_installers/cuda-repo-wsl-ubuntu-12-2-local_12.2.2-1_amd64.deb
sudo dpkg -i cuda-repo-wsl-ubuntu-12-2-local_12.2.2-1_amd64.deb
sudo cp /var/cuda-repo-wsl-ubuntu-12-2-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda


# Install python 3.10
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt -y install python3.10
apt -y install python3-pip

# Install Python requirements
pip install -r /run/requirements.txt




