import yaml
import time


def GetInfoMsg():
    infoMsg = "One or more yaml files are used to configure the swarm.\r\n"
    infoMsg += "The yaml file 'swarm-management.yml' is used by default if no other files are specified.\r\n"
    infoMsg += "A yaml file may be specified by adding '-file' or '-f' to the arguments.\r\n"
    infoMsg += "Example: -f swarm-management-stacks.yml -f swarm-management-networks.yml\r\n"
    infoMsg += "Environment variables may be set with environment files.\r\n"
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


def GetYamlData(yamlFiles):
    yamlStrings = ""
    for yamlFile in yamlFiles:
        yamlStrings += GetYamlString(yamlFile)
    yamlData = yaml.load(yamlStrings)
    if yamlData == None:
        errorMsg = "No .yml files where discovered!\r\n"
        errorMsg += GetInfoMsg()
        raise Exception(errorMsg)
    return yamlData


def GetArgumentValues(arguments, argumentType, ignoreArgumentsWithPrefix = "-"):
    argumentValues = []
    for i in range(len(arguments)-1):
        currentArgumentType = arguments[i]
        argumentValue = arguments[i+1]
        if currentArgumentType == argumentType and not(argumentValue.startswith(ignoreArgumentsWithPrefix)):
            argumentValues.append(argumentValue)
    return argumentValues


def GetSwarmManagementYamlData(arguments):
    yamlFiles = GetArgumentValues(arguments, '-file')
    yamlFiles += GetArgumentValues(arguments, '-f')
    if len(yamlFiles) == 0:
        yamlFiles.append('swarm-management.yml')
    yamlData = GetYamlData(yamlFiles)
    return yamlData


def GetEnvironmnetVariablesFiles(arguments):
    swarmManagementYamlData = GetSwarmManagementYamlData(arguments)
    envFiles = []
    if 'env_files' in swarmManagementYamlData:
        envFiles += swarmManagementYamlData['env_files']
    envFiles += GetArgumentValues(arguments, '-env')
    envFiles += GetArgumentValues(arguments, '-e')
    return envFiles


def GetProperties(arguments, propertyType, errorInfoMsg):
    swarmManagementYamlData = GetSwarmManagementYamlData(arguments)
    properties = {}
    if propertyType in swarmManagementYamlData:
        properties = swarmManagementYamlData[propertyType]
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
