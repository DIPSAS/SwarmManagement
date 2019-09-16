import unittest
from SwarmManagement import SwarmTools

class TestSwarmTools(unittest.TestCase):

    def test_getInforMsg_success(self):
        self.assertIsNotNone(SwarmTools.GetInfoMsg())

    def test_getArgumentValues_specific_selections(self):
        runSelections = ['run1', 'run2', 'run3']
        buildSelections = ['build1', 'build2']
        arguments = ['-run'] + runSelections + ['-build'] + buildSelections
        print(arguments)
        selectedRuns = SwarmTools.GetArgumentValues(arguments, '-run')
        selectedBuilds = SwarmTools.GetArgumentValues(arguments, '-build')
        print(selectedRuns)
        print(selectedBuilds)
        self.assertEqual(len(runSelections), len(selectedRuns))
        self.assertEqual(len(buildSelections), len(selectedBuilds))
        self.assertListEqual(runSelections, selectedRuns)
        self.assertListEqual(buildSelections, selectedBuilds)

    def test_getArgumentValues_common_selections(self):
        selections = ['selection1', 'selection2', 'selection3']
        arguments = ['-run'] + ['-build'] + selections
        print(arguments)
        selectedRuns = SwarmTools.GetArgumentValues(arguments, '-run')
        selectedBuilds = SwarmTools.GetArgumentValues(arguments, '-build')
        print(selectedRuns)
        print(selectedBuilds)
        self.assertEqual(len(selections), len(selectedRuns))
        self.assertListEqual(selections, selectedRuns)
        self.assertEqual(len(selections), len(selectedBuilds))
        self.assertListEqual(selections, selectedBuilds)


if __name__ == '__main__':
    unittest.main()
