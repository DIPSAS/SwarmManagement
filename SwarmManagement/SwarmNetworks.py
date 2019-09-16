from SwarmManagement import SwarmTools
from DockerBuildSystem import DockerSwarmTools, YamlTools
import sys


def GetInfoMsg():
    infoMsg = "Networks is configured by adding a 'networks' property to the .yaml file.\r\n"
    infoMsg += "The 'networks' property is a dictionary of networks.\r\n"
    infoMsg += "Each key in the network dictionary is the network name, as such: \r\n"
    infoMsg += "<network_name>:\r\n"
    infoMsg += "Example: \r\n"
    infoMsg += "networks: <network_name>:\r\n"
    infoMsg += "Create or remove a network by adding '-network -c/-create <network_name>' or 'network -rm/-remove <network_name>' to the arguments\r\n"
    infoMsg += "Create or remove all networks by adding '-network -c/-create all' or 'network -rm/-remove all' to the arguments\r\n"
    return infoMsg


def GetNetworks(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(arguments)
    return YamlTools.GetProperties('networks', yamlData)


def CreateNetworks(networksToCreate, networks):
    for networkToCreate in networksToCreate:
        if networkToCreate == 'all':
            for network in networks:
                CreateNetwork(network, networks[network])    
        else:
            if networkToCreate in networks:
                CreateNetwork(networkToCreate, networks[networkToCreate])


def CreateNetwork(networkName, networkProperties):
    if networkProperties == None:
        networkProperties = {}
    elif isinstance(networkProperties, bool):
        networkProperties = {'encrypted': networkProperties}

    encrypted = YamlTools.TryGetFromDictionary(networkProperties, 'encrypted', False)
    driver = YamlTools.TryGetFromDictionary(networkProperties, 'driver', 'overlay')
    attachable = YamlTools.TryGetFromDictionary(networkProperties, 'attachable', True)
    options = YamlTools.TryGetFromDictionary(networkProperties, 'options', [])

    DockerSwarmTools.CreateSwarmNetwork(
        networkName, encrypted, driver, attachable, options)


def RemoveNetworks(networksToRemove, networks):
    for networkToRemove in networksToRemove:
        if networkToRemove == 'all':
            for network in networks:
                RemoveNetwork(network)
        else:
            if networkToRemove in networks:
                RemoveNetwork(networkToRemove)


def RemoveNetwork(networkName):
    DockerSwarmTools.RemoveSwarmNetwork(networkName)


def HandleNetworks(arguments):
    if len(arguments) == 0:
        return
    if not('-network' in arguments):
        return

    if '-help' in arguments:
        print(GetInfoMsg())
        return

    networksToCreate = SwarmTools.GetArgumentValues(arguments, '-create')
    networksToCreate += SwarmTools.GetArgumentValues(arguments, '-c')

    networksToRemove = SwarmTools.GetArgumentValues(arguments, '-remove')
    networksToRemove += SwarmTools.GetArgumentValues(arguments, '-rm')

    networks = GetNetworks(arguments)

    CreateNetworks(networksToCreate, networks)
    RemoveNetworks(networksToRemove, networks)
    

if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleNetworks(arguments)
