#!/bin/bash

sudo apt-get update
sudo apt-get install -y python3-venv
python3 -m venv deadenv
source deadenv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
