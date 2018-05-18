from SwarmManagement import SwarmTools
from DockerBuildSystem import DockerSwarmTools
import sys


def GetInfoMsg():
    infoMsg = "Networks is configured by adding a 'networks' property to the .yaml file.\r\n"
    infoMsg += "The 'networks' property consists of a list of networks.\r\n"
    infoMsg += "Each item in the networks list is a list with the network name and a boolean to flag encrypted (true) or non-encrypted (false), as such: \r\n"
    infoMsg += "['<network_name>', true/false]\r\n"
    infoMsg += "Example: \r\n"
    infoMsg += "networks: [ ['first_network.txt', true], ['second_network', false]]\r\n"
    infoMsg += "Create or remove a network by adding '-network -c/-create <network_name>' or 'network -r/-remove <network_name>' to the arguments\r\n"
    infoMsg += "Create or remove all networks by adding '-network -c/-create --all' or 'network -r/-remove --all' to the arguments\r\n"
    return infoMsg


def GetNetworks(arguments):
    return SwarmTools.GetProperties(arguments, 'networks', GetInfoMsg())


def FindMatchingNetworks(secretName, secrets):
    return SwarmTools.FindMatchingProperty(secretName, secrets, GetInfoMsg())


def CreateNetworks(networksToCreate, networks):
    for networkToCreate in networksToCreate:
        if networkToCreate == '--all':
            for network in networks:
                CreateNetwork(network)    
        else:
            network = FindMatchingNetworks(networkToCreate, networks)
            CreateNetwork(network)


def CreateNetwork(network):
    if network != None:
        networkName = network[0]
        encrypted = network[1]
        DockerSwarmTools.CreateSwarmNetwork(
            networkName, encrypted)


def RemoveNetworks(networksToRemove, networks):
    for networkToRemove in networksToRemove:
        if networkToRemove == '--all':
            for network in networks:
                RemoveNetwork(network)
        else:
            network = FindMatchingNetworks(networkToRemove, networks)
            RemoveNetwork(network)


def RemoveNetwork(network):
    if network != None:
        networkName = network[0]
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
    networksToRemove += SwarmTools.GetArgumentValues(arguments, '-r')

    networks = GetNetworks(arguments)

    CreateNetworks(networksToCreate, networks)
    RemoveNetworks(networksToRemove, networks)
    

if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleNetworks(arguments)
