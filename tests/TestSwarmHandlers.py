import unittest
import os
from tests import TestTools
from SwarmManagement import SwarmConfigs
from SwarmManagement import SwarmSecrets
from SwarmManagement import SwarmVolumes
from SwarmManagement import SwarmNetworks
from SwarmManagement import SwarmStacks
from SwarmManagement import SwarmManager

class TestSwarmHandlers(unittest.TestCase):

    def test_a_config(self):
        print('EXECUTING SWARM CONFIG TEST')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        arguments = ['-config', '-create', 'all']
        SwarmConfigs.HandleConfigs(arguments)
        arguments = ['-config', '-rm', 'all']
        SwarmConfigs.HandleConfigs(arguments)
        arguments = ['-config', '-create', 'site.conf']
        SwarmConfigs.HandleConfigs(arguments)
        arguments = ['-config', '-rm', 'site.conf']
        SwarmConfigs.HandleConfigs(arguments)
        os.chdir(cwd)
        print('DONE EXECUTING SWARM CONFIG TEST')

    def test_b_secret(self):
        print('EXECUTING SWARM SECRET TEST')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        arguments = ['-secret', '-create', 'all']
        SwarmSecrets.HandleSecrets(arguments)
        arguments = ['-secret', '-rm', 'all']
        SwarmSecrets.HandleSecrets(arguments)
        arguments = ['-secret', '-create', 'site.key']
        SwarmSecrets.HandleSecrets(arguments)
        arguments = ['-secret', '-rm', 'site.key']
        SwarmSecrets.HandleSecrets(arguments)
        os.chdir(cwd)
        print('DONE EXECUTING SWARM SECRET TEST')

    def test_c_networks(self):
        print('EXECUTING SWARM NETWORK TEST')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        arguments = ['-network', '-create', 'all']
        SwarmNetworks.HandleNetworks(arguments)
        arguments = ['-network', '-rm', 'all']
        SwarmNetworks.HandleNetworks(arguments)
        arguments = ['-network', '-create', 'frontend_network']
        SwarmNetworks.HandleNetworks(arguments)
        arguments = ['-network', '-rm', 'frontend_network']
        SwarmNetworks.HandleNetworks(arguments)
        os.chdir(cwd)
        print('DONE EXECUTING SWARM NETWORK TEST')

    def test_d_volumes(self):
        print('EXECUTING SWARM VOLUMES TEST')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        arguments = ['-volume', '-create', 'all']
        SwarmVolumes.HandleVolumes(arguments)
        arguments = ['-volume', '-rm', 'all']
        SwarmVolumes.HandleVolumes(arguments)
        arguments = ['-volume', '-create', 'first_volume']
        SwarmVolumes.HandleVolumes(arguments)
        arguments = ['-volume', '-rm', 'first_volume']
        SwarmVolumes.HandleVolumes(arguments)
        os.chdir(cwd)
        print('DONE EXECUTING SWARM VOLUMES TEST')

    def test_e_manager(self):
        print('EXECUTING SWARM MANAGER TEST')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        arguments = ['-start']
        SwarmManager.HandleManagement(arguments)
        arguments = ['-restart', '2']
        SwarmManager.HandleManagement(arguments)
        arguments = ['-restart']
        SwarmManager.HandleManagement(arguments)
        arguments = ['-stop']
        SwarmManager.HandleManagement(arguments)
        os.chdir(cwd)
        print('DONE EXECUTING SWARM MANAGER TEST')

    def test_f_stacks(self):
        print('EXECUTING SWARM STACKS TEST')
        cwd = TestTools.ChangeToSampleFolderAndGetCwd()
        arguments = ['-start']
        SwarmManager.HandleManagement(arguments)
        arguments = ['-stack', '-deploy', 'all']
        SwarmStacks.HandleStacks(arguments)
        arguments = ['-stack', '-rm', 'all']
        SwarmStacks.HandleStacks(arguments)
        arguments = ['-stack', '-deploy', 'ssl_proxy']
        SwarmStacks.HandleStacks(arguments)
        arguments = ['-stack', '-rm', 'ssl_proxy']
        SwarmStacks.HandleStacks(arguments)
        arguments = ['-stop']
        SwarmManager.HandleManagement(arguments)
        os.chdir(cwd)
        print('DONE EXECUTING SWARM STACKS TEST')

if __name__ == '__main__':
    unittest.main()