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
                        "hosts": ['babbage.ug.eie.wits.ac.za', 'testing.ug.eie.wits.ac.za'],
                        "yos": "2"}
        expected_user = {"username": "guneap",
                         "gid_number": "2000",
                         "login_shell": "/bin/bash",
                         "first_name": "Gunea",
                         "last_name": "Pig",
                         "yos": "2",
                         "hosts": ['babbage.ug.eie.wits.ac.za', 'testing.ug.eie.wits.ac.za'],
                         "home_directory": "/home/ug/guneap",
                         "uid_number": "2000",
                         "email": ["123@students.wits.ac.za"]}
        if users.find_one(user_to_save['username']):
            users.delete(user=user_to_save)
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

    def test_add_host(self):
        """ Can I add a host?"""
        original_group = {"name": "natsuki", "members": ['mandla']}

        guneap = {"username": "guneap",
                  "first_name": "Gunea",
                  "last_name": "Pig",
                  "email": ["123@students.wits.ac.za"],
                  "password": "passing",
                  "hosts": ['babbage.ug.eie.wits.ac.za'],
                  "yos": "2"}
        expected_guneap = {"username": "guneap",
                           "gid_number": "2000",
                           "login_shell": "/bin/bash",
                           "first_name": "Gunea",
                           "last_name": "Pig",
                           "yos": "2",
                           "hosts": ['babbage.ug.eie.wits.ac.za', 'testing.ug.eie.wits.ac.za'],
                           "home_directory": "/home/ug/guneap",
                           "uid_number": "2000",
                           "email": ["123@students.wits.ac.za"]}
        johnd = {"username": "johnd",
                  "first_name": "John",
                  "last_name": "Doe",
                  "email": ["john.doe@students.wits.ac.za"],
                  "password": "passing",
                  "yos": "4"}
        expected_johnd = {"username": "johnd",
                           "gid_number": "4000",
                           "login_shell": "/bin/bash",
                           "first_name": "John",
                           "last_name": "Doe",
                           "yos": "4",
                           "hosts": ['babbage.ug.eie.wits.ac.za'],
                           "home_directory": "/home/ug/johnd",
                           "uid_number": "4063",
                           "email": ["john.doe@students.wits.ac.za"]}
        already_member = johnd['username']
        existing_user = guneap['username']
        new_member = guneap['username']
        non_existing_user = "poiqaalkj"
        babbage = "babbage.ug.eie.wits.ac.za"
        testing = "testing.ug.eie.wits.ac.za"

        # remove from a group that exists
        user = users.find_one("guneap")
        if user:
            users.delete("guneap")
        self.assertTrue(users.save(guneap)) # save with one host
        user = users.find_one("mandla")
        if user:
            users.delete("johnd")
        self.assertTrue(users.save(johnd)) # no groups

        users.add_host(guneap['username'], babbage) # already there
        users.add_host(guneap['username'], testing)# new host for guneap
        g = users.find_one(guneap['username'])
        self.assertEquals(g, expected_guneap)
        users.add_host(johnd['username'], babbage) # has no hosts
        j = users.find_one(johnd['username'])
        self.assertEquals(j, expected_johnd)

        # what if user does not exist
        with self.assertRaises(ValueError):
            users.add_host(non_existing_user, babbage) # has no hosts

    def test_remove_host(self):
        guneap = {"username": "guneap",
                  "first_name": "Gunea",
                  "last_name": "Pig",
                  "email": ["123@students.wits.ac.za"],
                  "password": "passing",
                  "hosts": ['babbage.ug.eie.wits.ac.za', 'testing.ug.eie.wits.ac.za'],
                  "yos": "2"}
        expected_guneap = {"username": "guneap",
                           "gid_number": "2000",
                           "login_shell": "/bin/bash",
                           "first_name": "Gunea",
                           "last_name": "Pig",
                           "yos": "2",
                           "hosts": ['babbage.ug.eie.wits.ac.za'],
                           "home_directory": "/home/ug/guneap",
                           "uid_number": "2000",
                           "email": ["123@students.wits.ac.za"]}
        non_existing_user = "poiqaalkj"
        babbage = "babbage.ug.eie.wits.ac.za"
        testing = "testing.ug.eie.wits.ac.za"

        # prepare
        user = users.find_one("guneap")
        if user:
            users.delete("guneap")
        self.assertTrue(users.save(guneap)) # save with one host

        # remove a host
        users.remove_host(guneap['username'], testing)
        g = users.find_one(guneap['username'])
        self.assertEquals(g, expected_guneap)

        # remove a host thats not there
        users.remove_host(guneap['username'], testing)
        self.assertEquals(g, expected_guneap)

        # remove the last host
        users.remove_host(guneap['username'], babbage)
        g = users.find_one(guneap['username'])
        del(expected_guneap['hosts'])
        self.assertEquals(g, expected_guneap)

        # remove from a user that does not exists
        with self.assertRaises(ValueError):
            users.remove_host(non_existing_user, babbage) # has no hosts

    def test_change_password(self):
        """ I can change password """
        mandla = users.find_one('mandla')
        self.assertTrue(users.change_password('mandla', None, 'passing'))

if __name__ == "__main__":
    unittest.main()
