# Install python and pip as described here:
# https://matthewhorne.me/how-to-install-python-and-pip-on-windows-10/

pip install SwarmManagement
pip install pyopenssl

cd DockerSSLProxy
python SSLKeyGenerator.py
cd ..

SwarmManagement -start