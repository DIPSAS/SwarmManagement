# Docker Swarm Management
Swarm Management is an executable python application, installed with pip.
The application makes it easy to manage a Docker Swarm by configuring a single *.yml file describing which stacks to deploy, and which networks, configs or secrets to create.

## Example
1. Install SwarmManagement with pip:
    - pip install SwarmManagement
2. Create a `swarm-management.yml` file describing all properties of the swarm.
    - The `swarm-management.yml` file contains following properties:
        - stacks: [ [`<compose_file>`, `<stack_name>`] ]
        - networks: [ [`<network_name>`, `<true/false>` => encrypted (true) / non-encrypted (false)] ]
        - configs: [ [`<config_file>`, `<config_name>`] ]
        - secrets: [ [`<secret_file>`, `<secret_name>`] ]
        - env_file: path_to/*.env
3. Manage Swarm
    - Start Swarm with:
        - -> SwarmManagement start
    - Stop Swarm with:
        - -> SwarmManagement stop
    - SwarmManagement uses the `swarm-management.yml` file by default to configure the swarm.
    - Additional info is found by asking SwarmManagement:
        - -> SwarmManagement -help

Please have a look at an example of use here:
- https://github.com/DIPSAS/SwarmManagement/tree/master/example

## Install And/Or Upgrade
- pip install --no-cache-dir --upgrade SwarmManagement

## Prerequisites
- Docker:
    - https://www.docker.com/get-docker

## Additional Info
- The pip package may be located at:
    - https://pypi.org/project/SwarmManagement

## Publish New Version.
1. Configure setup.py with new version.
2. Build: python setup.py bdist_wheel
3. Publish: twine upload dist/*