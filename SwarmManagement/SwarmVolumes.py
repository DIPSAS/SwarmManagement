from SwarmManagement import SwarmTools
from DockerBuildSystem import DockerSwarmTools
import sys


def GetInfoMsg():
    infoMsg = "Volumes is configured by adding a 'volumes' property to the .yaml file.\r\n"
    infoMsg += "The 'volumes' property is a dictionary of volumes.\r\n"
    infoMsg += "Each key in the volume dictionary is the volume name, as such: \r\n"
    infoMsg += "<volume_name>:\r\n"
    infoMsg += "Example: \r\n"
    infoMsg += "volumes: <volume_name>:\r\n"
    infoMsg += "Create or remove a volume by adding '-volume -c/-create <volume_name>' or '-volume -rm/-remove <volume_name>' to the arguments\r\n"
    infoMsg += "Create or remove all volumes by adding '-volume -c/-create all' or '-volume -rm/-remove all' to the arguments\r\n"
    return infoMsg


def GetVolumes(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(arguments)
    return SwarmTools.GetProperties(arguments, 'volumes', GetInfoMsg(), yamlData)


def CreateVolumes(volumesToCreate, volumes):
    for volumeToCreate in volumesToCreate:
        if volumeToCreate == 'all':
            for volume in volumes:
                CreateVolume(volume)
        else:
            if volumeToCreate in volumes:
                CreateVolume(volumeToCreate)


def CreateVolume(volumeName):
    DockerSwarmTools.CreateSwarmVolume(volumeName)


def RemoveVolumes(volumesToRemove, volumes):
    for volumeToRemove in volumesToRemove:
        if volumeToRemove == 'all':
            for volume in volumes:
                RemoveVolume(volume)
        else:
            if volumeToRemove in volumes:
                RemoveVolume(volumeToRemove)


def RemoveVolume(volumeName):
    DockerSwarmTools.RemoveSwarmVolume(volumeName)


def HandleVolumes(arguments):
    if len(arguments) == 0:
        return
    if not('-volume' in arguments):
        return

    if '-help' in arguments:
        print(GetInfoMsg())
        return
        
    volumesToCreate = SwarmTools.GetArgumentValues(arguments, '-create')
    volumesToCreate += SwarmTools.GetArgumentValues(arguments, '-c')

    volumesToRemove = SwarmTools.GetArgumentValues(arguments, '-remove')
    volumesToRemove += SwarmTools.GetArgumentValues(arguments, '-rm')

    volumes = GetVolumes(arguments)

    CreateVolumes(volumesToCreate, volumes)
    RemoveVolumes(volumesToRemove, volumes)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleVolumes(arguments)
