from SwarmManagement import SwarmTools
from DockerBuildSystem import DockerSwarmTools
import sys


def GetInfoMsg():
    infoMsg = "Stacks is configured by adding a 'stacks' property to the .yaml file.\r\n"
    infoMsg += "The 'stacks' property is a dictionary of stacks.\r\n"
    infoMsg += "Each key in the stack dictionary is the stack name with a value containing the path to the compose file, as such: \r\n"
    infoMsg += "<stack_name>: <compose_file>\r\n"
    infoMsg += "Example: \r\n"
    infoMsg += "stacks: <stack_name>: <compose_file>\r\n"
    infoMsg += "Deploy or remove a stack by adding '-stack -d/-deploy <stack_name>' or 'stack -r/-remove <stack_name>' to the arguments\r\n"
    infoMsg += "Deploy or remove all stacks by adding '-stack -d/-deploy --all' or 'stack -r/-remove --all' to the arguments\r\n"
    return infoMsg


def GetStacks(arguments):
    return SwarmTools.GetProperties(arguments, 'stacks', GetInfoMsg())


def DeployStacks(stacksToDeploy, stacks, environmentFile):
    for stackToDeploy in stacksToDeploy:
        if stackToDeploy == '--all':
            for stack in stacks:
                DeployStack(stack, stacks[stack], environmentFile)
        else:
            if stackToDeploy in stacks:
                DeployStack(stackToDeploy, stacks[stackToDeploy], environmentFile)


def DeployStack(stackName, composeFile, environmentFiles):
    DockerSwarmTools.DeployStack(
        composeFile, stackName, environmentFiles)


def RemoveStacks(stacksToRemove, stacks):
    for stackToRemove in stacksToRemove:
        if stackToRemove == '--all':
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
    stacksToRemove += SwarmTools.GetArgumentValues(arguments, '-r')

    stacks = GetStacks(arguments)
    environmentFiles = SwarmTools.GetEnvironmnetVariablesFiles(arguments)

    DeployStacks(stacksToDeploy, stacks, environmentFiles)
    RemoveStacks(stacksToRemove, stacks)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleStacks(arguments)
