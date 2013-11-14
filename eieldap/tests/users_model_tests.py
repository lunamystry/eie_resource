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

    def test_get_next_uid(self):
        """ Manual test, can I get the next uid """
        next_uid = Users.next_uid_number(1)
        # check that its withing 1000 - 1999

        # raises an error if the number of valid uids has been reached

if __name__ == "__main__":
    unittest.main()
