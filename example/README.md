# Example Of Use With Swarm Management
1. Install dependencies in requirements.txt with pip
2. Generate ssl keys
    - -> cd DockerSSLProxy
    - -> python SSLKeyGenerator.py
    - -> cd ..
3. Start Swarm
    - -> SwarmManagement start
    - SwarmManagement uses the swarm-management.yml file to configure the swarm.
    - Stop the swarm with:
        - -> SwarmManagement stop
    - Additional Info is found by asking SwarmManagement:
        - -> SwarmManagement -help
