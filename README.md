# Docker Swarm Management

[![PyPI version](https://badge.fury.io/py/SwarmManagement.svg)](https://badge.fury.io/py/SwarmManagement)
[![Build Status](https://travis-ci.com/DIPSAS/SwarmManagement.svg?branch=master)](https://travis-ci.com/DIPSAS/SwarmManagement)
[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)

Swarm Management is a python application, installed with pip.
The application makes it easy to manage a Docker Swarm by configuring a single *.yml file describing which stacks to deploy, and which networks, configs or secrets to create.

## Install Or Upgrade
- pip install --upgrade SwarmManagement

## Verify Installation
- `swm -help`

## Example
1. Create a `swarm.management.yml` file describing all properties of the swarm.
    - The `swarm.management.yml` file contains following properties:
    ```yaml
    stacks:
        <stack_name>: <compose_file>
    networks:
        <network_name>: 
            encrypted: false
            driver: overlay
            attachable: true
            options:
              - --ipv6
    configs:
        <config_name>: <config_file>
    secrets:
        <secret_name>: <secret_file>
    volumes:
        <volume_name>:
            driver: local
            driverOptions:
              - type=tmpfs
              - device=tmpfs
              - o=size=100m,uid=1000
    env_files:
        - <environment_file>
    ```

2. Manage Swarm:
    - Start Swarm with:
        - -> swm -start
    - Stop Swarm with:
        - -> swm -stop
    - Restart Swarm with:
        - -> swm -restart
    - Deploy/Update or Remove a single stack:
        - -> swm -stack -deploy `<stack_name>`
        - -> swm -stack -remove `<stack_name>`
        - Or deploy/remove all stacks with the `all` attribute:
            - -> swm -stack -deploy all
            - -> swm -stack -remove all
    - Create or Remove a single network:
        - -> swm -network -create `<network_name>`
        - -> swm -network -remove `<network_name>`
        - Or create/remove all networks with the `all` attribute:
            - -> swm -network -create all
            - -> swm -network -remove all
    - Create or Remove a single config:
        - -> swm -config -create `<config_name>`
        - -> swm -config -remove `<config_name>`
        - Or create/remove all configs with the `all` attribute:
            - -> swm -stack -create all
            - -> swm -stack -remove all
    - Create or Remove a single secret:
        - -> swm -secret -create `<secret_name>`
        - -> swm -secret -remove `<secret_name>`
        - Or create/remove all secrets with the `all` attribute:
            - -> swm -secret -create all
            - -> swm -secret -remove all
    - Create or Remove a single volume:
        - -> swm -volume -create `<volume_name>`
        - -> swm -volume -remove `<volume_name>`
        - Or create/remove all volumes with the `all` attribute:
            - -> swm -volume -create all
            - -> swm -volume -remove all
    - SwarmManagement uses the `swarm.management.yml` file by default to configure the swarm.
        - Specify a single or multiple *.yml files to use for configuring the swarm using the `-f` attribute:
            - -> swm -start -f swarm-stacks.yml -f swarm-networks.yml
    - Additional info is found by asking SwarmManagement:
        - -> swm -help
        - -> swm -stack -help
        - -> swm -network -help
        - -> swm -config -help
        - -> swm -secret -help
        - -> swm -volume -help

Please have a look at an example of use here:
- https://github.com/DIPSAS/SwarmManagement/tree/master/example

## Section Features

## Start/Stop or Restart Swarm
Deploy the swarm with `swm -start`, and stop the swarm with `swm -stop`.
Restart the swarm with `swm -restart <restart_delay_in_seconds>`. The `<restart_delay_in_seconds>` argument is optional, and defaults to 10 seconds if not given.

### Stacks
The `stacks` section lists all stacks to be deployed as: `<stack_name>: <compose_file>`

### Networks
The `networks` section lists all networks to be created as, and each network is created with the following default properties:
* `encrypted: false`
* `driver: overlay`
* `attachable: true`
* `options:`
    - `<list_of_network_options>`

### Configs
The `configs` section lists all configs to be created as: `<config_name>: <config_file>`

### Secrets
The `secrets` section lists all secrets to be created as: `<secret_name>: <secret_file>`

### Volumes
The `volumes` section lists all volumes to be created as, and each volumes is created with the following default properties:
* `driver: local`
* `driverOptions:`
    - `<list_of_driver_options>`

### Environment variables
The `env_files` section lists all environmnet (`.env`) files with environment variables to expose.
By convention, a present `.env` file will automatically be loaded.

## Prerequisites
- Docker:
    - https://www.docker.com/get-docker
- Install Dependencies:
    - pip install -r requirements.txt

## Additional Info
- The pip package may be located at:
    - https://pypi.org/project/SwarmManagement

## Publish New Version.
1. Configure setup.py with new version.
2. Build: python setup.py bdist_wheel
3. Publish: twine upload dist/*

## Run Unit Tests
- python -m unittest