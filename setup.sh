#!/bin/bash

pip install -r requirements.txt
sudo touch /var/log/namerdbin.log
sudo chown $USER:$USER /var/log/namerdbin.log
