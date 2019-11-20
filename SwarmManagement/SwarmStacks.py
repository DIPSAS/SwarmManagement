from SwarmManagement import SwarmTools
from DockerBuildSystem import DockerSwarmTools, YamlTools
import sys


def GetInfoMsg():
    infoMsg = "Stacks is configured by adding a 'stacks' property to the .yaml file.\r\n"
    infoMsg += "The 'stacks' property is a dictionary of stacks.\r\n"
    infoMsg += "Each key in the stack dictionary is the stack name with a value containing the path to the compose file, as such: \r\n"
    infoMsg += "<stack_name>: <compose_file>\r\n"
    infoMsg += "Example: \r\n"
    infoMsg += "stacks: <stack_name>: <compose_file>\r\n"
    infoMsg += "Deploy or remove a stack by adding '-stack -d/-deploy <stack_name>' or 'stack -rm/-remove <stack_name>' to the arguments\r\n"
    infoMsg += "Deploy or remove all stacks by adding '-stack -d/-deploy all' or 'stack -rm/-remove all' to the arguments\r\n"
    return infoMsg


def GetStacks(arguments):
    yamlData = SwarmTools.LoadYamlDataFromFiles(arguments)
    return YamlTools.GetProperties('stacks', yamlData)


def DeployStacks(stacksToDeploy, stacks, environmentFiles):
    for stackToDeploy in stacksToDeploy:
        if stackToDeploy == 'all':
            for stack in stacks:
                DeployStack(stack, stacks[stack], environmentFiles)
        else:
            if stackToDeploy in stacks:
                DeployStack(stackToDeploy, stacks[stackToDeploy], environmentFiles)


def DeployStack(stackName, composeFile, environmentFiles):
    DockerSwarmTools.DeployStack(
        composeFile, stackName, environmentFiles, withRegistryAuth=True)


def RemoveStacks(stacksToRemove, stacks):
    for stackToRemove in stacksToRemove:
        if stackToRemove == 'all':
            for stack in stacks:
                RemoveStack(stack)
        else:
            if stackToRemove in stacks:
                RemoveStack(stackToRemove)


def RemoveStack(stack):
    DockerSwarmTools.RemoveStack(stack)


def HandleStacks(arguments):
    if len(arguments) == 0:
        return
    if not('-stack' in arguments):
        return

    if '-help' in arguments:
        print(GetInfoMsg())
        return

    stacksToDeploy = SwarmTools.GetArgumentValues(arguments, '-deploy')
    stacksToDeploy += SwarmTools.GetArgumentValues(arguments, '-d')

    stacksToRemove = SwarmTools.GetArgumentValues(arguments, '-remove')
    stacksToRemove += SwarmTools.GetArgumentValues(arguments, '-rm')

    stacks = GetStacks(arguments)
    yamlData = SwarmTools.LoadYamlDataFromFiles(arguments)
    environmentFiles = SwarmTools.GetEnvironmnetVariablesFiles(arguments, yamlData)

    DeployStacks(stacksToDeploy, stacks, environmentFiles)
    RemoveStacks(stacksToRemove, stacks)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleStacks(arguments)
