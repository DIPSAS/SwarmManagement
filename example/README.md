# Example Of Use With Swarm Management
1. Install dependencies in requirements.txt with pip
2. Generate ssl keys
    - -> cd DockerSSLProxy
    - -> python SSLKeyGenerator.py
    - -> cd ..
3. Manage Swarm
    - Start Swarm with:
        - -> SwarmManagement start
    - Stop Swarm with:
        - -> SwarmManagement stop
    - SwarmManagement uses the `swarm-management.yml` file by default to configure the swarm.
    - Additional info is found by asking SwarmManagement:
        - -> SwarmManagement -help