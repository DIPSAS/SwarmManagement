from SwarmManagement import SwarmTools
from DockerBuildSystem import DockerSwarmTools
import sys


def GetInfoMsg():
    infoMsg = "Stacks is configured by adding a 'stacks' property to the .yaml file.\r\n"
    infoMsg += "The 'stacks' property consists of a list of stacks.\r\n"
    infoMsg += "Each item in the stack list is a list with a path to the compose file and the stack name, as such: \r\n"
    infoMsg += "['<compose_file>', '<stack_name>']\r\n"
    infoMsg += "Example: \r\n"
    infoMsg += "stacks: [ ['compose_file_first_stack.yml', 'first_stack'], ['compose_file_second_stack.yml', 'second_stack'] ]\r\n"
    infoMsg += "Deploy or remove a stack by adding '-stack -d/-deploy <stack_name>' or 'stack -r/-remove <stack_name>' to the arguments\r\n"
    infoMsg += "Deploy or remove all stacks by adding '-stack -d/-deploy --all' or 'stack -r/-remove --all' to the arguments\r\n"
    return infoMsg


def GetStacks(arguments):
    return SwarmTools.GetProperties(arguments, 'stacks', GetInfoMsg())


def FindMatchingStack(stackName, stacks):
    return SwarmTools.FindMatchingProperty(stackName, stacks, GetInfoMsg())


def DeployStacks(stacksToDeploy, stacks, environmentFile):
    for stackToDeploy in stacksToDeploy:
        if stackToDeploy == '--all':
            for stack in stacks:
                DeployStack(stack, environmentFile)
        else:
            stack = FindMatchingStack(stackToDeploy, stacks)
            DeployStack(stack, environmentFile)


def DeployStack(stack, environmentFile):
    if stack != None:
        composeFile = stack[0]
        stackName = stack[1]
        DockerSwarmTools.DeployStack(
            composeFile, stackName, environmentFile)


def RemoveStacks(stacksToRemove, stacks):
    for stackToRemove in stacksToRemove:
        if stackToRemove == '--all':
            for stack in stacks:
                RemoveStack(stack)
        else:
            stack = FindMatchingStack(stackToRemove, stacks)
            RemoveStack(stack)


def RemoveStack(stack):
    if stack != None:
        stackName = stack[1]
        DockerSwarmTools.RemoveStack(stackName)


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
    environmentFile = SwarmTools.GetEnvironmnetVariablesFile(arguments)

    DeployStacks(stacksToDeploy, stacks, environmentFile)
    RemoveStacks(stacksToRemove, stacks)
    

if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleStacks(arguments)
