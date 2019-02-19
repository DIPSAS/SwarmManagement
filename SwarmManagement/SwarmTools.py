import yaml
import time
import re
import os
from DockerBuildSystem import TerminalTools


DEFAULT_SWARM_MANAGEMENT_YAML_FILE = 'swarm-management.yml'
DEFAULT_ENVIRONMENT_FILE = '.env'


def GetInfoMsg():
    infoMsg = "One or more yaml files are used to configure the swarm.\r\n"
    infoMsg += "The yaml file 'swarm-management.yml' is used by default if no other files are specified.\r\n"
    infoMsg += "A yaml file may be specified by adding '-file' or '-f' to the arguments.\r\n"
    infoMsg += "Example: -f swarm-management-stacks.yml -f swarm-management-networks.yml\r\n"
    infoMsg += "Environment variables may be set with environment files.\r\n"
    infoMsg += GetEnvironmentVariablesInfoMsg()
    return infoMsg


def GetEnvironmentVariablesInfoMsg():
    infoMsg = "Environment variables may be set with environment files.\r\n"
    infoMsg += "Multiple environment files may be set set with the 'env_files' property in the yaml file.\r\n"
    infoMsg += "Example: \r\n"
    infoMsg += "env_files: \r\n"
    infoMsg += "\t - 'environment.env'\r\n"
    infoMsg += "A preceding listed file will override any matching variables from the file listed above.\r\n"
    infoMsg += "Environment files may also be set set with the -e/-env argument.\r\n"
    infoMsg += "Setting the -e/-env argument will override matching environment variables in the files from the 'env_files' yaml property.\r\n"
    infoMsg += "Example: -e environment.env\r\n"
    return infoMsg


def GetYamlString(yamlFile):
    with open(yamlFile) as f:
        yamlString = f.read() + "\r\n"
    return yamlString


def DumpYamlDataToFile(yamlData, yamlFile):
    yamlDump = yaml.dump(yamlData)
    with open(yamlFile, 'w') as f:
        f.write(yamlDump)


def HandleDumpYamlData(arguments, defaultYamlFiles=[DEFAULT_SWARM_MANAGEMENT_YAML_FILE]):
    if not('>' in arguments):
        return
    outputFiles = GetArgumentValues(arguments, '>')
    for outputFile in outputFiles:
        yamlData = LoadYamlDataFromFiles(arguments, defaultYamlFiles)
        DumpYamlDataToFile(yamlData, outputFile)


def ReplaceEnvironmentVariablesMatches(yamlString):
    pattern = r'\$\{([^}^{]+)\}'
    matches = re.finditer(pattern, yamlString)
    for match in matches:
        envVar = match.group()[2:-1]
        envValue = os.environ.get(envVar)
        if envValue == None:
            envValue = ''
        yamlString = yamlString.replace(match.group(), envValue)
    return yamlString


def GetYamlData(yamlFiles, ignoreEmptyYamlData = False):
    yamlStrings = ""
    for yamlFile in yamlFiles:
        yamlStrings += GetYamlString(yamlFile)
    yamlStrings = ReplaceEnvironmentVariablesMatches(yamlStrings)
    yamlData = yaml.load(yamlStrings)
    if yamlData == None:
        if ignoreEmptyYamlData:
            yamlData = {}
            return yamlData
        errorMsg = "No yml data where discovered!\r\n"
        errorMsg += GetInfoMsg()
        raise Exception(errorMsg)
    return yamlData


def GetArgumentValues(arguments, argumentType, ignoreArgumentsWithPrefix = "-", getFirstAlternativeOnly = True):
    argumentValues = []
    for i in range(len(arguments)):
        currentArgumentType = arguments[i]
        if currentArgumentType == argumentType:
            for j in range(i, len(arguments)):
                argumentValue = arguments[j]
                if not(argumentValue.startswith(ignoreArgumentsWithPrefix)):
                    argumentValues.append(argumentValue)
                    if getFirstAlternativeOnly:
                        return argumentValues
    return argumentValues


def LoadYamlDataFromFiles(arguments, defaultYamlFiles=[DEFAULT_SWARM_MANAGEMENT_YAML_FILE], \
    ignoreNonExistingFiles = False, ignoreEmptyYamlData = False):
    yamlFiles = GetArgumentValues(arguments, '-file')
    yamlFiles += GetArgumentValues(arguments, '-f')
    if len(yamlFiles) == 0:
        yamlFiles = defaultYamlFiles
    if ignoreNonExistingFiles:
        yamlFiles = RemoveNonExistingFiles(yamlFiles)
    yamlData = GetYamlData(yamlFiles, ignoreEmptyYamlData)
    return yamlData


def RemoveNonExistingFiles(files):
    existingFiles = []
    for filename in files:
        if os.path.isfile(filename):
            existingFiles.append(filename)
    return existingFiles


def LoadEnvironmentVariables(arguments, defaultYamlFiles=[DEFAULT_SWARM_MANAGEMENT_YAML_FILE]):
    yamlData = LoadYamlDataFromFiles(
        arguments, defaultYamlFiles, True, True)
    environmentFiles = GetEnvironmnetVariablesFiles(
        arguments, yamlData)
    for environmentFile in environmentFiles:
        TerminalTools.LoadEnvironmentVariables(environmentFile)


def GetEnvironmnetVariablesFiles(arguments, yamlData):
    envFiles = []
    if 'env_files' in yamlData:
        envFiles += yamlData['env_files']
    envFiles += GetArgumentValues(arguments, '-env')
    envFiles += GetArgumentValues(arguments, '-e')
    if os.path.isfile(DEFAULT_ENVIRONMENT_FILE):
        envFiles += [DEFAULT_ENVIRONMENT_FILE]
    return envFiles


def GetProperties(arguments, propertyType, errorInfoMsg, yamlData):
    properties = {}
    if propertyType in yamlData:
        properties = yamlData[propertyType]
    return properties


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
