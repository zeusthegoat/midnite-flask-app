#!/bin/bash
sudo apt-get update -y
sudo apt-get install -y python3-pip git

cd /home/ubuntu
git clone https://github.com/zeusthegoat/midnite-alert-api.git
cd midnite-alert-api
pip3 install -r requirements.txt

nohup python3 app.py > output.log 2>&1 &