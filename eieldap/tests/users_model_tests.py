from mock import patch, Mock
from eieldap.models import Users
import unittest


class UsersTestCase(unittest.TestCase):
    def test_save(self):
        """ Create a new user """
        user_to_save = {"name": "Leonard", "members": ['mandla', 'leny']}

    def test_update(self):
        """ Can I update a user? I hope so"""
        pass

if __name__ == "__main__":
    unittest.main()
