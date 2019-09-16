from SwarmManagement import SwarmTools
from DockerBuildSystem import DockerSwarmTools, YamlTools
import sys


def GetInfoMsg():
    infoMsg = "Configs is configured by adding a 'configs' property to the .yaml file.\r\n"
    infoMsg += "The 'configs' property is a dictionary of configs.\r\n"
    infoMsg += "Each key in the config dictionary is the config name with a value containing the path to the config file, as such: \r\n"
    infoMsg += "<config_name>: <config_file>\r\n"
    infoMsg += "Example: \r\n"
    infoMsg += "configs: <config_name>: <config_file>\r\n"
    infoMsg += "Create or remove a config by adding '-config -c/-create <config_name>' or '-config -rm/-remove <config_name>' to the arguments\r\n"
    infoMsg += "Create or remove all configs by adding '-config -c/-create all' or '-config -rm/-remove all' to the arguments\r\n"
    return infoMsg


def GetConfigs(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(arguments)
    return YamlTools.GetProperties('configs', yamlData)


def CreateConfigs(configsToCreate, configs):
    for configToCreate in configsToCreate:
        if configToCreate == 'all':
            for config in configs:
                CreateConfig(config, configs[config])
        else:
            if configToCreate in configs:
                CreateConfig(configToCreate, configs[configToCreate])


def CreateConfig(configName, configFile):
    DockerSwarmTools.CreateSwarmConfig(
        configFile, configName)


def RemoveConfigs(configsToRemove, configs):
    for configToRemove in configsToRemove:
        if configToRemove == 'all':
            for config in configs:
                RemoveConfig(config)
        else:
            if configToRemove in configs:
                RemoveConfig(configToRemove)


def RemoveConfig(configName):
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
    configsToRemove += SwarmTools.GetArgumentValues(arguments, '-rm')

    configs = GetConfigs(arguments)

    CreateConfigs(configsToCreate, configs)
    RemoveConfigs(configsToRemove, configs)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleConfigs(arguments)
