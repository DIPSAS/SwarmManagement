import unittest
import os
import random
from .. import SwarmTools

class TestSwarmTools(unittest.TestCase):

    def test_getInforMsg_success(self):
        self.assertIsNotNone(SwarmTools.GetInfoMsg())

    def test_getArgumentValues_success(self):
        runSelections = ['run1', 'run2', 'run3']
        buildSelections = ['build1', 'build2']
        arguments = ['-run'] + runSelections + ['-build'] + buildSelections
        selectedRuns = SwarmTools.GetArgumentValues(arguments, '-run')
        selectedBuilds = SwarmTools.GetArgumentValues(arguments, '-build')
        print(selectedRuns)
        print(selectedBuilds)
        self.assertEqual(len(runSelections), len(selectedRuns))
        self.assertEqual(len(buildSelections), len(selectedBuilds))
        self.assertListEqual(runSelections, selectedRuns)
        self.assertListEqual(buildSelections, selectedBuilds)

    def test_replaceEnvironmentVariablesMatches_success(self):
        ENV_KEY = "ENVIRONMENT_KEY_" + str(random.randint(0, 1000))
        ENV_VALUE = "ENVIRONMENT VALUE"
        os.environ.setdefault(ENV_KEY, ENV_VALUE)
        yamlString = 'testing string ${' + ENV_KEY + '} should be replaced'
        print(yamlString)
        replacedYamlString = SwarmTools.ReplaceEnvironmentVariablesMatches(yamlString)
        print(replacedYamlString)
        self.assertTrue(ENV_VALUE in replacedYamlString)


if __name__ == '__main__':
    unittest.main()
