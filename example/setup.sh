#!/bin/sh

# Editing in windows ads '\r' to the file, which linux dislikes.
# Remove all carriage return for all files in current folder by using following command in linux:
# -> sed -i 's/\r//g' *.sh

# Run in linux/ubuntu with:
#   -> ./setup.sh

sudo pip install -r requirements.txt

cd DockerSSLProxy
python SSLKeyGenerator.py
cd ..

SwarmManagement start