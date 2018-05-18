from SwarmManagement import SwarmTools
from DockerBuildSystem import DockerSwarmTools
import sys


def GetInfoMsg():
    infoMsg = "Secrets is configured by adding a 'secrets' property to the .yaml file.\r\n"
    infoMsg += "The 'secrets' property consists of a list of secrets.\r\n"
    infoMsg += "Each item in the secrets list is a list with a path to the secret file and the secret name, as such: \r\n"
    infoMsg += "['<secret_file', '<secret_name>']\r\n"
    infoMsg += "Example: \r\n"
    infoMsg += "secrets: [ ['first_secret_file.txt', 'first_secret'], ['second_secret_file.txt', 'second_secret'] ]\r\n"
    infoMsg += "Create or remove a secret by adding '-secret -c/-create <secret_name>' or 'secret -r/-remove <secret_name>' to the arguments\r\n"
    infoMsg += "Create or remove all secrets by adding '-secret -c/-create --all' or 'secret -r/-remove --all' to the arguments\r\n"
    return infoMsg


def GetSecrets(arguments):
    return SwarmTools.GetProperties(arguments, 'secrets', GetInfoMsg())


def FindMatchingSecret(secretName, secrets):
    return SwarmTools.FindMatchingProperty(secretName, secrets, GetInfoMsg())


def CreateSecrets(secretsToCreate, secrets):
    for secretToCreate in secretsToCreate:
        if secretToCreate == '--all':
            for secret in secrets:
                CreateSecret(secret)
        else:
            secret = FindMatchingSecret(secretToCreate, secrets)
            CreateSecret(secret)


def CreateSecret(secret):
    if secret != None:
        secretFile = secret[0]
        secretName = secret[1]
        DockerSwarmTools.CreateSwarmSecret(
            secretFile, secretName)


def RemoveSecrets(secretsToRemove, secrets):
    for secretToRemove in secretsToRemove:
        if secretToRemove == '--all':
            for secret in secrets:
                RemoveSecret(secret)
        else:
            secret = FindMatchingSecret(secretToRemove, secrets)
            RemoveSecret(secret)


def RemoveSecret(secret):
    if secret != None:
        secretName = secret[1]
        DockerSwarmTools.RemoveSwarmSecret(secretName)


def HandleSecrets(arguments):
    if len(arguments) == 0:
        return
    if not('-secret' in arguments):
        return

    if '-help' in arguments:
        print(GetInfoMsg())
        return

    secretsToCreate = SwarmTools.GetArgumentValues(arguments, '-create')
    secretsToCreate += SwarmTools.GetArgumentValues(arguments, '-c')

    secretsToRemove = SwarmTools.GetArgumentValues(arguments, '-remove')
    secretsToRemove += SwarmTools.GetArgumentValues(arguments, '-r')

    secrets = GetSecrets(arguments)

    CreateSecrets(secretsToCreate, secrets)
    RemoveSecrets(secretsToRemove, secrets)


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleSecrets(arguments)
