from mock import patch, Mock
from eieldap.models import users
import unittest


class usersTestCase(unittest.TestCase):
    def test_save(self):
        """ Create a new user """
        user_to_save = {"username": "guneap",
                        "first_name": "Gunea",
                        "last_name": "Pig",
                        "email": "guneap@students.wits.ac.za",
                        "password": "passing",
                        "yos": "1"}
        expected_user = {"name": "natsuki", "members": ['mandla', 'leny']}
        ignored_user = {"name": "natsuki", "members": ['mandla', 'leny']}
        invalid_user = {"name": "navina"}

        with self.assertRaises(TypeError):
            users.save(invalid_user)

        # Does not exist
        if users.find_one(user_to_save['username']):
            users.delete(user=user_to_save)
        self.assertTrue(users.save(user_to_save))

        # exists
        user_to_save = {"username": "guneap",
                        "first_name": "Gunea",
                        "last_name": "Pig",
                        "email": "123@students.wits.ac.za",
                        "password": "passing",
                        "yos": "2"}
        expected_user = {"username": "guneap",
                         "gid_number": "2000",
                         "login_shell": "/bin/bash",
                         "first_name": "Gunea",
                         "last_name": "Pig",
                         "yos": "2",
                         "home_directory": "/home/ug/guneap",
                         "uid_number": "1000",
                         "email": ["123@students.wits.ac.za"]}
        self.assertTrue(users.save(user_to_save))
        user = users.find_one("guneap")
        self.assertEquals(user, expected_user)

    def test_get_next_uid(self):
        """ Manual test, can I get the next uid """
        # check that its withing range
        for yos in range(1, 8):
            next_uid = users.next_uid_number(yos)
            start = yos*1000
            end = start + 1000;
            self.assertTrue(next_uid in range(start, end))

        with self.assertRaises(ValueError):
            next_uid = users.next_uid_number(-1)
        with self.assertRaises(ValueError):
            next_uid = users.next_uid_number(8)

        # raises an error if the number of valid uids has been reached


if __name__ == "__main__":
    unittest.main()
