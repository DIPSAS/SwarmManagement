import yaml
import time


def GetInfoMsg():
    infoMsg = "One or more yaml files are used to configure the swarm.\r\n"
    infoMsg += "The yaml file 'swarm-management.yml' is used by default if no other files are specified.\r\n"
    infoMsg += "A yaml file may be specified by adding '-file' or '-f' to the arguments.\r\n"
    infoMsg += "Example: -f swarm-management-stacks.yml -f swarm-management-networks.yml\r\n"
    infoMsg += "Environment variables may be set with an environment file.\r\n"
    infoMsg += "The environment file may be set set with the 'env_files' property in the yaml file.\r\n"
    infoMsg += "Example: env_files: ['environment.env']\r\n"
    infoMsg += "The environment file may also be set set with the -e/-env argument.\r\n"
    infoMsg += "Setting the -e/-env argument will override the 'env_files' yaml file property.\r\n"
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


def GetArgumentValues(arguments, argumentType):
    argumentValues = []
    for i in range(len(arguments)-1):
        currentArgumentType = arguments[i]
        argumentValue = arguments[i+1]
        if currentArgumentType == argumentType:
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
    envFiles = GetArgumentValues(arguments, '-env')
    envFiles += GetArgumentValues(arguments, '-e')
    if len(envFiles) == 0:
        swarmManagementYamlData = GetSwarmManagementYamlData(arguments)
        if 'env_files' in swarmManagementYamlData:
            envFiles = swarmManagementYamlData['env_files']
    return envFiles


def GetProperties(arguments, propertyType, errorInfoMsg):
    swarmManagementYamlData = GetSwarmManagementYamlData(arguments)
    secrets = []
    if propertyType in swarmManagementYamlData:
        secrets = swarmManagementYamlData[propertyType]
    if not(isinstance(secrets, list)):
        raise Exception(errorInfoMsg)
    return secrets


def FindMatchingProperty(propertyName, properties, errorInfoMsg):
    for propertyValue in properties:
        if not(isinstance(propertyValue, list)):
            errorMsg = "The yaml property must be a list!\r\n"
            errorMsg += errorInfoMsg
            raise Exception(errorMsg)
        if len(propertyValue) != 2:
            errorMsg = "The yaml property must be a list with size of 2!\r\n"
            errorMsg += errorInfoMsg
            raise Exception(errorMsg)
        matchpropertyName = propertyValue[1]
        if matchpropertyName == propertyName:
            return propertyValue
    return None


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
