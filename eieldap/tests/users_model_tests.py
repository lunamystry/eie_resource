from mock import patch, Mock
from eieldap.models import Users
import unittest


class UsersTestCase(unittest.TestCase):
    def test_save(self):
        """ Create a new user """
        user_to_save = {"username": "guneap",
                        "first_name": "Gunea",
                        "last_name": "Pig",
                        "email": "guneap@students.wits.ac.za",
                        "password": "secret",
                        "yos": "1"}
        expected_user = {"name": "natsuki", "members": ['mandla', 'leny']}
        ignored_user = {"name": "natsuki", "members": ['mandla', 'leny']}
        invalid_user = {"name": "navina"}

        # with self.assertRaises(TypeError):
        #     models.Users.save(invalid_user)

        # Does not exist
        # Users.delete(user=user_to_save)
        self.assertTrue(Users.save(user_to_save))

        # exists
        # user_to_save = {"name": "natsuki", "members": ['mandla', 'leonard']}
        # expected_user = {"name": "natsuki", "members": ['mandla', 'leonard']}
        # self.assertTrue(models.Users.save(user_to_save))
        # user = models.Users.find_one("natsuki")
        # self.assertEquals(user, expected_user)


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
