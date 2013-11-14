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
        # check that its withing range
        for yos in range(1, 8):
            next_uid = Users.next_uid_number(yos)
            start = yos*1000
            end = start + 1000;
            self.assertTrue(next_uid in range(start, end))

        with self.assertRaises(ValueError):
            next_uid = Users.next_uid_number(-1)
        with self.assertRaises(ValueError):
            next_uid = Users.next_uid_number(8)

        # raises an error if the number of valid uids has been reached
if __name__ == "__main__":
    unittest.main()
