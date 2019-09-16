import sys
from SwarmManagement import SwarmStacks, SwarmConfigs, SwarmSecrets, SwarmNetworks, SwarmVolumes, SwarmTools
from DockerBuildSystem import DockerSwarmTools


def GetInfoMsg():
    infoMsg = "Manage Docker Swarm\r\n"
    infoMsg += "Add '-start' to arguments to start swarm with all stacks deployed and properties created (networks, secrets, configs..).\r\n"
    infoMsg += "Add '-stop' to arguments to stop swarm with all stacks and properties removed.\r\n"
    infoMsg += "Add '-restart' to arguments to restart swarm.\r\n"
    infoMsg += "Otherwise:\r\n\r\n"
    infoMsg += "Deploy Or Remove Stacks:\r\n"
    infoMsg += SwarmStacks.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Create Or Remove Networks:\r\n"
    infoMsg += SwarmNetworks.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Create Or Remove Configs:\r\n"
    infoMsg += SwarmConfigs.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Create Or Remove Secrets:\r\n"
    infoMsg += SwarmSecrets.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Create Or Remove Volumes:\r\n"
    infoMsg += SwarmVolumes.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Additional Info:\r\n"
    infoMsg += SwarmTools.GetInfoMsg() + "\r\n\r\n"
    infoMsg += "Add '-help' to arguments to print this info again.\r\n\r\n"
    return infoMsg


def StartSwarm(arguments):
    DockerSwarmTools.StartSwarm()
    SwarmVolumes.HandleVolumes(['-volume', '-create', 'all'] + arguments)
    SwarmConfigs.HandleConfigs(['-config', '-create', 'all'] + arguments)
    SwarmSecrets.HandleSecrets(['-secret', '-create', 'all'] + arguments)
    SwarmNetworks.HandleNetworks(['-network', '-create', 'all'] + arguments)
    SwarmStacks.HandleStacks(['-stack', '-deploy', 'all'] + arguments)


def StopSwarm(arguments):
    SwarmStacks.HandleStacks(['-stack', '-remove', 'all'] + arguments)
    SwarmConfigs.HandleConfigs(['-config', '-remove', 'all'] + arguments)
    SwarmSecrets.HandleSecrets(['-secret', '-remove', 'all'] + arguments)
    # SwarmNetworks.HandleNetworks(['-network', '-remove', 'all'] + arguments)


def RestartSwarm(arguments):
    StopSwarm(arguments)
    secTimeout = 10
    restartArguments = SwarmTools.GetArgumentValues(arguments, '-restart')
    if len(restartArguments) > 0 and restartArguments[0].isdigit():
        secTimeout = int(restartArguments[0])
    SwarmTools.TimeoutCounter(secTimeout)
    StartSwarm(arguments)


def HandleManagement(arguments):
    if len(arguments) == 0:
        print(GetInfoMsg())
        return

    SwarmTools.LoadEnvironmentVariables(arguments)
    SwarmTools.HandleDumpYamlData(arguments)
    
    if '-help' in arguments \
        and not('-stack' in arguments) \
        and not('-config' in arguments) \
        and not('-secret' in arguments) \
        and not('-network' in arguments):
        print(GetInfoMsg())
    elif '-start' in arguments:
        StartSwarm(arguments)
    elif '-stop' in arguments:
        StopSwarm(arguments)
    elif '-restart' in arguments:
        RestartSwarm(arguments)
    else:
        SwarmVolumes.HandleVolumes(arguments)
        SwarmConfigs.HandleConfigs(arguments)
        SwarmSecrets.HandleSecrets(arguments)
        SwarmNetworks.HandleNetworks(arguments)
        SwarmStacks.HandleStacks(arguments)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleManagement(arguments)
