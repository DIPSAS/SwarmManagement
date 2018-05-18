# Example Of Use With Swarm Management
1. Install dependencies in requirements.txt with pip
2. Generate ssl keys
    - -> cd DockerSSLProxy
    - -> python SSLKeyGenerator.py
    - -> cd ..
3. Manage Swarm
    - Start the Swarm with:
        - -> SwarmManagement start
    - Stop the Swarm with:
        - -> SwarmManagement stop
    - SwarmManagement uses the `swarm-management.yml` file by default to configure the swarm.
    - Additional Info is found by asking SwarmManagement:
        - -> SwarmManagement -help