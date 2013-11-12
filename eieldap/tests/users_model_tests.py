from mock import patch, Mock
from eieldap.manager import Manager
import unittest
import tempfile


class UsersTestCase(unittest.TestCase):
    def test_create(self):
        """ Create a new user """
        pass

    @patch.object(Manager, 'find_one')
    def test_update(self, find_one):
        """ Can I update a user? I hope so"""
        pass

if __name__ == "__main__":
    unittest.main()
