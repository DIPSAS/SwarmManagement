import time
import os
import sys
from DockerBuildSystem import TerminalTools, YamlTools

DEFAULT_ENVIRONMENT_FILE = '.env'
DEFAULT_SWARM_MANAGEMENT_YAML_FILES = [
    'swarm.management.yml', 
    'swarm.management.yaml',
    'swarm-management.yml',
    'swarm-management.yaml']


def GetInfoMsg():
    infoMsg = "One or more yaml files are used to configure the swarm.\r\n"
    infoMsg += "The yaml file 'swarm.management.yml' is used by default if no other files are specified.\r\n"
    infoMsg += "A yaml file may be specified by adding '-file' or '-f' to the arguments.\r\n"
    infoMsg += "Example: -f swarm.management-stacks.yml -f swarm.management-networks.yml\r\n"
    infoMsg += "Environment variables may be set with environment files.\r\n"
    infoMsg += GetEnvironmentVariablesInfoMsg()
    infoMsg += GetYamlDumpInfoMsg()
    return infoMsg


def GetEnvironmentVariablesInfoMsg():
    infoMsg = "Environment variables may be set with environment files or variables directly.\r\n"
    infoMsg += "Multiple environment files or variables may be set set with the 'env_files' property in the yaml file.\r\n"
    infoMsg += "Example: \r\n"
    infoMsg += "env_files: \r\n"
    infoMsg += "\t - 'environment.env'\r\n"
    infoMsg += "\t - 'envKey=envValue'\r\n"
    infoMsg += "Topmost listed files will override any matching variables from the file listed below.\r\n"
    infoMsg += "Directly setting a variable will always override an existing matching variable.\r\n"
    infoMsg += "Environment files and variables may also be set set with the -e/-env argument.\r\n"
    infoMsg += "Example: -e environment.env envKey=envValue\r\n"
    return infoMsg


def GetYamlDumpInfoMsg():
    infoMsg = "It is possible to dump current yaml data using the '-dump' argument.\r\n"
    infoMsg += "Example: -dump output.yml\r\n"
    return infoMsg


def GetNoYmlFilesFoundMsg(defaultYamlFiles=DEFAULT_SWARM_MANAGEMENT_YAML_FILES):
    infoMsg = "Error\r\n"
    infoMsg += "Could not find any supported management files.\r\n"
    infoMsg += "Are you in the right directory?\r\n"
    infoMsg += "Supported management files: " + str.join(', ', defaultYamlFiles) + "\r\n"
    return infoMsg


def AssertYamlFilesExists(yamlFiles, defaultYamlFiles=DEFAULT_SWARM_MANAGEMENT_YAML_FILES):
    existingYamlFiles = []
    for yamlFile in yamlFiles:
        if os.path.isfile(yamlFile):
            existingYamlFiles.append(yamlFile)
    
    if len(existingYamlFiles) == 0:
        print(GetNoYmlFilesFoundMsg(defaultYamlFiles))
        exit(-1)

    return existingYamlFiles


def HandleDumpYamlData(arguments, defaultYamlFiles=DEFAULT_SWARM_MANAGEMENT_YAML_FILES):
    if not('-dump' in arguments):
        return
    outputFiles = GetArgumentValues(arguments, '-dump')
    for outputFile in outputFiles:
        yamlData = LoadYamlDataFromFiles(arguments, defaultYamlFiles)
        YamlTools.DumpYamlDataToFile(yamlData, outputFile)


def GetArgumentValues(arguments, argumentType, ignoreArgumentsWithPrefix="-", stopAtFirstArgumentWithPrefix="-"):
    argumentValues = []
    for i in range(len(arguments)):
        currentArgumentType = arguments[i]
        if currentArgumentType == argumentType:
            for j in range(i, len(arguments)):
                argumentValue = arguments[j]
                if not(argumentValue.startswith(ignoreArgumentsWithPrefix)):
                    argumentValues.append(argumentValue)
                elif argumentValue != argumentType and \
                    len(argumentValues) > 0 and \
                    argumentValue.startswith(stopAtFirstArgumentWithPrefix):
                    return argumentValues
    return argumentValues


def LoadYamlDataFromFiles(arguments, defaultYamlFiles=DEFAULT_SWARM_MANAGEMENT_YAML_FILES, \
    ignoreEmptyYamlData = False):
    yamlFiles = GetArgumentValues(arguments, '-file')
    yamlFiles += GetArgumentValues(arguments, '-f')
    if len(yamlFiles) == 0:
        yamlFiles = defaultYamlFiles
    yamlFiles = AssertYamlFilesExists(yamlFiles, defaultYamlFiles)
    yamlData = YamlTools.GetYamlData(yamlFiles, ignoreEmptyYamlData, infoMsgOnError=GetInfoMsg())
    return yamlData


def LoadEnvironmentVariables(arguments, defaultYamlFiles=DEFAULT_SWARM_MANAGEMENT_YAML_FILES):
    yamlData = LoadYamlDataFromFiles(
        arguments, defaultYamlFiles, True)
    environmentFiles = GetEnvironmnetVariablesFiles(
        arguments, yamlData)
    for environmentFile in environmentFiles:
        if os.path.isfile(environmentFile):
            TerminalTools.LoadEnvironmentVariables(environmentFile)
        elif '=' in environmentFile:
            key, value = environmentFile.split('=')
            os.environ[key] = value



def GetEnvironmnetVariablesFiles(arguments, yamlData):
    envFiles = []
    envFiles += GetArgumentValues(arguments, '-env')
    envFiles += GetArgumentValues(arguments, '-e')
    if 'env_files' in yamlData:
        envFiles += yamlData['env_files']
    if os.path.isfile(DEFAULT_ENVIRONMENT_FILE):
        envFiles += [DEFAULT_ENVIRONMENT_FILE]
    return envFiles


def TimeoutCounter(secTimeout):
    startTime = time.time()
    elapsedTime = time.time() - startTime
    timeLeft = secTimeout - int(elapsedTime)
    printedTime = timeLeft
    while elapsedTime < secTimeout:
        timeLeft = secTimeout - int(elapsedTime)
        if timeLeft < printedTime:
            printedTime = timeLeft
            print("Restarting Swarm in %d seconds" % printedTime)
        elapsedTime = time.time() - startTime


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleDumpYamlData(arguments)
