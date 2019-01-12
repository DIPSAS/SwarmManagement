from SwarmManagement import SwarmTools
from DockerBuildSystem import DockerSwarmTools
import sys


def GetInfoMsg():
    infoMsg = "Networks is configured by adding a 'networks' property to the .yaml file.\r\n"
    infoMsg += "The 'networks' property is a dictionary of networks.\r\n"
    infoMsg += "Each key in the network dictionary is the network name with a value containing a boolean to flag encrypted (true) or non-encrypted (false), as such: \r\n"
    infoMsg += "<network_name>: true/false\r\n"
    infoMsg += "Example: \r\n"
    infoMsg += "secrets: <network_name>: true/false\r\n"
    infoMsg += "Create or remove a network by adding '-network -c/-create <network_name>' or 'network -rm/-remove <network_name>' to the arguments\r\n"
    infoMsg += "Create or remove all networks by adding '-network -c/-create all' or 'network -rm/-remove all' to the arguments\r\n"
    return infoMsg


def GetNetworks(arguments):
    return SwarmTools.GetProperties(arguments, 'networks', GetInfoMsg())


def CreateNetworks(networksToCreate, networks):
    for networkToCreate in networksToCreate:
        if networkToCreate == 'all':
            for network in networks:
                CreateNetwork(network, networks[network])    
        else:
            if networkToCreate in networks:
                CreateNetwork(networkToCreate, networks[networkToCreate])


def CreateNetwork(networkName, encrypted):
    DockerSwarmTools.CreateSwarmNetwork(
        networkName, encrypted)


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
