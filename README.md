# Docker Swarm Management
Swarm Management is a python application, installed with pip.
The application makes it easy to manage a Docker Swarm by configuring a single *.yml file describing which stacks to deploy, and which networks, configs or secrets to create.

## Example
1. Install SwarmManagement with pip:
    - pip install SwarmManagement
2. Create a `swarm-management.yml` file describing all properties of the swarm.
    - The `swarm-management.yml` file contains following properties:
        - stacks: [ [`<compose_file>`, `<stack_name>`], .. ]
        - networks: [ [`<network_name>`, `<true/false>` => encrypted (true) / non-encrypted (false)], .. ]
        - configs: [ [`<config_file>`, `<config_name>`], .. ]
        - secrets: [ [`<secret_file>`, `<secret_name>`], .. ]
        - env_files: [ `<environment_file>`, .. ]
3. Manage Swarm
    - Start Swarm with:
        - -> SwarmManagement -start
    - Stop Swarm with:
        - -> SwarmManagement -stop
    - Restart Swarm with:
        - -> SwarmManagement -restart
    - Deploy/Update or Remove a single stack:
        - -> SwarmManagement -stack -deploy `<stack_name>`
        - -> SwarmManagement -stack -remove `<stack_name>`
        - Or deploy/remove all stacks with the `--all` attribute:
            - -> SwarmManagement -stack -deploy --all
            - -> SwarmManagement -stack -remove --all
    - Create or Remove a single network:
        - -> SwarmManagement -network -create `<network_name>`
        - -> SwarmManagement -network -remove `<network_name>`
        - Or create/remove all networks with the `--all` attribute:
            - -> SwarmManagement -network -create --all
            - -> SwarmManagement -network -remove --all
    - Create or Remove a single config:
        - -> SwarmManagement -config -create `<config_name>`
        - -> SwarmManagement -config -remove `<config_name>`
        - Or create/remove all configs with the `--all` attribute:
            - -> SwarmManagement -stack -create --all
            - -> SwarmManagement -stack -remove --all
    - Create or Remove a single secret:
        - -> SwarmManagement -secret -create `<secret_name>`
        - -> SwarmManagement -secret -remove `<secret_name>`
        - Or create/remove all secrets with the `--all` attribute:
            - -> SwarmManagement -secret -create --all
            - -> SwarmManagement -secret -remove --all
    - SwarmManagement uses the `swarm-management.yml` file by default to configure the swarm.
        - Specify a single or multiple *.yml files to use for configuring the swarm using the `-f` attribute:
            - -> SwarmManagement -start -f swarm-stacks.yml -f swarm-networks.yml
    - Additional info is found by asking SwarmManagement:
        - -> SwarmManagement -help
        - -> SwarmManagement -stack -help
        - -> SwarmManagement -network -help
        - -> SwarmManagement -config -help
        - -> SwarmManagement -secret -help

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