#!/bin/bash

echo "■環境構築------------------------------------"
pip install --upgrade pip
sudo yum -y update
sudo yum -y install python27 # Installs Python 2.7.
sudo yum -y install python36 # Installs Python 3.6.
curl -O https://bootstrap.pypa.io/get-pip.py # Get the install script.
sudo python get-pip.py                       # Install pip.
rm get-pip.py                                # Delete the install script.
sudo python -m pip install boto3
echo "■githubから必要な資材を取得する------------------"
git clone https://github.com/ryoishim/LINExAWSServerless.git
