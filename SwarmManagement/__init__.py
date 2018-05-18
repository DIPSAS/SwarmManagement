from SwarmManagement import SwarmManager
import sys

def RemoveInvalidArguments(arguments):
    if len(arguments) == 0:
        return arguments
    elif arguments[0] == 'python' or '.py' in arguments[0]:
        arguments = arguments[1:]
        arguments = RemoveInvalidArguments(arguments)
    return arguments

def main():
    """Entry point for the application script"""
    arguments = sys.argv[1:]
    print('Managing Swarm with arguments: ')
    print(arguments)
    arguments = RemoveInvalidArguments(arguments)
    if len(arguments) == 0:
        arguments = ['-help']
    SwarmManager.HandleManagement(arguments)
