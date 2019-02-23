import unittest
import os
from .. import SwarmTools

class TestSwarmTools(unittest.TestCase):

    def test_getInforMsg_success(self):
        self.assertIsNotNone(SwarmTools.GetInfoMsg())


if __name__ == '__main__':
    unittest.main()