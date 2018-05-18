import sys
import time
from SwarmManagement import SwarmStacks, SwarmConfigs, SwarmSecrets, SwarmNetworks, SwarmTools
from DockerBuildSystem import DockerSwarmTools


def GetInfoMsg():
    infoMsg = "Manage Docker Swarm\r\n"
    infoMsg += "Add 'start' to arguments to start swarm with all stacks deployed and properties created (networks, secrets, configs..).\r\n"
    infoMsg += "Add 'stop' to arguments to stop swarm with all stacks and properties removed.\r\n"
    infoMsg += "Add 'restart' to arguments to restart swarm.\r\n"
    infoMsg += "Otherwise:\r\n\r\n"
    infoMsg += "Deploy Or Remove Stacks:\r\n"
    infoMsg += SwarmStacks.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Create Or Remove Networks:\r\n"
    infoMsg += SwarmNetworks.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Create Or Remove Configs:\r\n"
    infoMsg += SwarmConfigs.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Create Or Remove Secrets:\r\n"
    infoMsg += SwarmSecrets.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Additional Info:\r\n"
    infoMsg += SwarmTools.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Add '-help' to arguments to print this info again.\r\n\r\n"
    return infoMsg


def StartSwarm():
    DockerSwarmTools.StartSwarm()
    SwarmConfigs.HandleConfigs(['config', '-create', '--all'])
    SwarmSecrets.HandleSecrets(['secret', '-create', '--all'])
    SwarmNetworks.HandleNetworks(['network', '-create', '--all'])
    SwarmStacks.HandleStacks(['stack', '-deploy', '--all'])


def StopSwarm():
    SwarmStacks.HandleStacks(['stack', '-remove', '--all'])
    SwarmConfigs.HandleConfigs(['config', '-remove', '--all'])
    SwarmSecrets.HandleSecrets(['secret', '-remove', '--all'])
    SwarmNetworks.HandleNetworks(['network', '-remove', '--all'])


def RestartSwarm():
    StopSwarm()
    secTimeout = 10
    SwarmTools.TimeoutCounter(secTimeout)
    StartSwarm()


def HandleManagement(arguments):
    if len(arguments) == 0:
        print(GetInfoMsg())
    
    if arguments[0] == '-help':
        print(GetInfoMsg())
    elif arguments[0] == 'start':
        StartSwarm()
    elif arguments[0] == 'stop':
        StopSwarm()
    elif arguments[0] == 'restart':
        RestartSwarm()
    else:
        SwarmConfigs.HandleConfigs(arguments)
        SwarmSecrets.HandleSecrets(arguments)
        SwarmNetworks.HandleNetworks(arguments)
        SwarmStacks.HandleStacks(arguments)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleManagement(arguments)
