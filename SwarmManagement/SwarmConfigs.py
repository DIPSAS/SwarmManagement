from SwarmManagement import SwarmTools
from DockerBuildSystem import DockerSwarmTools
import sys


def GetInfoMsg():
    infoMsg = "Configs is configured by adding a 'configs' property to the .yaml file.\r\n"
    infoMsg += "The 'config' property consists of a list of configs.\r\n"
    infoMsg += "Each item in the configs list is a list with a path to the config file and the config name, as such: \r\n"
    infoMsg += "['<config_file', '<config_name>']\r\n"
    infoMsg += "Example: \r\n"
    infoMsg += "configs: [ ['first_config_file.txt', 'first_config'], ['second_config_file.txt', 'second_config']]\r\n"
    infoMsg += "Create or remove a config by adding '-config -c/-create <config_name>' or '-config -r/-remove <config_name>' to the arguments\r\n"
    infoMsg += "Create or remove all configs by adding '-config -c/-create --all' or '-config -r/-remove --all' to the arguments\r\n"
    return infoMsg


def GetConfigs(arguments):
    return SwarmTools.GetProperties(arguments, 'configs', GetInfoMsg())


def FindMatchingConfig(configName, configs):
    return SwarmTools.FindMatchingProperty(configName, configs, GetInfoMsg())


def CreateConfigs(configsToCreate, configs):
    for configToCreate in configsToCreate:
        if configToCreate == '--all':
            for config in configs:
                CreateConfig(config)
        else:
            config = FindMatchingConfig(configToCreate, configs)
            CreateConfig(config)


def CreateConfig(config):
    if config != None:
        configFile = config[0]
        configName = config[1]
        DockerSwarmTools.CreateSwarmConfig(
            configFile, configName)


def RemoveConfigs(configsToRemove, configs):
    for configToRemove in configsToRemove:
        if configToRemove == '--all':
            for config in configs:
                RemoveConfig(config)
        else:
            config = FindMatchingConfig(configToRemove, configs)
            RemoveConfig(config)


def RemoveConfig(config):
    if config != None:
        configName = config[1]
        DockerSwarmTools.RemoveSwarmConfig(configName)


def HandleConfigs(arguments):
    if len(arguments) == 0:
        return
    if not('-config' in arguments):
        return

    if '-help' in arguments:
        print(GetInfoMsg())
        return
        
    configsToCreate = SwarmTools.GetArgumentValues(arguments, '-create')
    configsToCreate += SwarmTools.GetArgumentValues(arguments, '-c')

    configsToRemove = SwarmTools.GetArgumentValues(arguments, '-remove')
    configsToRemove += SwarmTools.GetArgumentValues(arguments, '-r')

    configs = GetConfigs(arguments)

    CreateConfigs(configsToCreate, configs)
    RemoveConfigs(configsToRemove, configs)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleConfigs(arguments)
