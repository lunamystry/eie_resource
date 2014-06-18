from eieldap.models import groups
from eieldap.models import users
import unittest


class groupsTestCase(unittest.TestCase):

    def setUp(self):
        self.existing_user = {"username": "janed",
                              "first_name": "Jane",
                              "last_name": "Doe",
                              "email": ["jane.doe@students.wits.ac.za"],
                              "password": "passing",
                              "hosts": ['dummy'],
                              "gid_number": "4000",
                              "uid_number": "4001",
                              "login_shell": "/bin/bash",
                              "home_directory": "/home/ug/janed",
                              "yos": "4"}
        self.existing_user2 = {"username": "johnd",
                               "first_name": "John",
                               "last_name": "Doe",
                               "email": ["john.doe@students.wits.ac.za"],
                               "password": "passing",
                               "hosts": ['dummy'],
                               "gid_number": "4000",
                               "uid_number": "4001",
                               "login_shell": "/bin/bash",
                               "home_directory": "/home/ug/johnd",
                               "yos": "4"}
        users.delete(self.existing_user['username'])
        users.delete(self.existing_user2['username'])
        users.add(self.existing_user)
        users.add(self.existing_user2)
        self.valid = {"name": "natsuki",
                      "gid_number": "1000",
                      "description": "Natsuki, like the summer",
                      "members": [self.existing_user['username']]}
        self.updated_valid = {"name": "natsuki",
                              "gid_number": "1000",
                              "description": "Natsuki, like the summer",
                              "members": [self.existing_user['username'],
                                          self.existing_user2['username']]}
        self.no_members = {"name": "navina"}
        self.empty_members = {"name": "navina", "members": []}

    def tearDown(self):
        users.delete(self.existing_user['username'])
        users.delete(self.existing_user2['username'])
        groups.delete(self.valid['name'])
        groups.delete(self.expected['name'])
        groups.delete(self.updated_valid['name'])

    def test_save_and_find_one(self):
        '''simple save of a valid group'''
        groups.save(self.valid)
        group = groups.find(self.valid['name'])
        self.assertEquals(group, self.valid)

    def test_save_with_user_not_in_directory(self):
        '''cannot save a group which has a member who is not in the LDAP dir'''
        with self.assertRaises(ValueError):
            invalid = {"name": "invalid", "members": ["not_there"]}
            groups.save(invalid)

    def test_save_a_group_that_exists(self):
        '''saving a group that exists, will update its members'''
        groups.save(self.valid)
        group = groups.find_one(self.valid['name'])
        self.assertEquals(group, self.valid)

    def test_save_updates_existing_group(self):
        '''saving a group that exists, will update its members'''
        groups.save(self.valid)
        group = groups.find_one(self.valid['name'])
        self.assertEquals(group, self.valid)

        groups.save(self.updated_valid)
        group = groups.find_one(self.valid['name'])
        self.assertEquals(group, self.updated_valid)


    def test_cant_save_group_with_no_members(self):
        ''' Because LDAP does not allow creating a group without members, I
        don't allow it either'''
        with self.assertRaises(ValueError):
            groups.save(self.no_members)

    def test_cant_save_group_with_empty_members(self):
        ''' Because LDAP does not allow creating a group without members, I
        don't allow it either'''
        with self.assertRaises(ValueError):
            groups.save(self.empty_members)

    def test_find_using_valid_group(self):
        groups.save(self.valid)
        group = groups.find_one(group=self.valid)
        self.assertEquals(group, self.valid)

    def test_find_a_non_existing_group(self):
        '''If a group does not exist, then None should be returned'''
        group = groups.find_one("qpoipwoqi")
        self.assertEquals(group, None)

    def test_find_can_specify_both_name_and_group(self):
        '''should use names if both name and group are given'''
        groups.save(self.valid)
        group = groups.find_one(name=self.valid['name'],
                                group=self.no_members)
        self.assertEquals(group, self.valid)

    def test_find_can_specify_wrong_name_and_correct_group(self):
        '''will return one group if attributes are valid'''
        groups.save(self.valid)
        group = groups.find_one(name='aslkajsa',
                                group=self.valid)
        self.assertEquals(group, self.valid)

    def test_find_None_if_both_name_and_group_are_None(self):
        '''If you a name or attribute are None, then None is returned'''
        group = groups.find_one(name=None, group=None)
        self.assertEquals(group, None)

    def test_delete_an_existing_group(self):
        ''' If a group exists, I should be able to delete it and not get it
        back '''
        groups.save(self.valid)
        groups.delete(self.valid['name'])
        group = groups.find_one(self.valid['name'])
        self.assertEquals(group, None)

    def test_delete_a_non_existing_group(self):
        ''' If a group does not exist, it does not matter, just pretend it was
        deleted'''
        groups.delete(self.valid['name'])
        group = groups.find_one(self.valid['name'])
        self.assertEquals(group, None)


class groupMembersTestCase(unittest.TestCase):
    def setUp(self):
        self.existing_user = {"username": "guneap",
                              "first_name": "Gunea",
                              "last_name": "Pig",
                              "email": "123@students.wits.ac.za",
                              "password": "secret",
                              "hosts": ['babbage.ug.eie.wits.ac.za'],
                              "yos": "3"}
        self.existing_user2 = {"username": "johnd",
                               "first_name": "John",
                               "last_name": "Doe",
                               "email": ["john.doe@students.wits.ac.za"],
                               "password": "passing",
                               "hosts": ['dummy'],
                               "gid_number": "4000",
                               "uid_number": "4001",
                               "login_shell": "/bin/bash",
                               "home_directory": "/home/ug/johnd",
                               "yos": "4"}
        users.delete(self.existing_user['username'])
        users.delete(self.existing_user2['username'])
        users.add(self.existing_user)
        users.add(self.existing_user2)
        self.existing_group = {"name": "natsuki",
                               "gid_number": "1000",
                               "description": "Natsuki, like the summer",
                               "members": [self.existing_user['username']]}
        groups.save(self.existing_group)
        self.non_existing_user = "poiqaalkj"
        groups.save(self.existing_group)
        self.new_member = {"username": "johnd",
                           "first_name": "John",
                           "last_name": "Doe",
                           "email": "mandla.niigata@students.wits.ac.za",
                           "password": "passing",
                           "hosts": ['dummy'],
                           "yos": "4"}

    def tearDown(self):
        users.delete(self.existing_user['username'])
        users.delete(self.existing_user2['username'])
        groups.delete(self.existing_group['name'])

    def test_add_member_new_member(self):
        '''I should be able to simply add new valid member'''
        groups.add_member(self.existing_group['name'],
                          self.existing_user['username'])

    def test_add_member_already_member(self):
        '''adding a username which is already there does nothing'''
        groups.add_member(self.existing_group['name'],
                          self.existing_user['username'])
        groups.add_member(self.existing_group['name'],
                          self.existing_user['username'])

    def test_add_member_non_existant_group(self):
        '''cannot add a username of a group who is not in the directory'''
        with self.assertRaises(ValueError):
            groups.add_member('not_there', 'not_there')

    def test_add_member_non_existant_user(self):
        '''cannot add a username of a user who is not in the directory'''
        with self.assertRaises(ValueError):
            groups.add_member(self.existing_group['name'], 'not_there')

    def test_remove_member(self):
        '''should be able to simply remove a member'''
        groups.add_member(self.existing_group['name'],
                          self.existing_user2['username'])
        groups.remove_member(self.existing_group['name'],
                             self.existing_user['username'])

    def test_remove_member_last_member(self):
        '''cannot remove the last member of a group'''
        with self.assertRaises(ReferenceError):
            groups.remove_member(self.existing_group['name'],
                                 self.existing_user['username'])

    def test_remove_member_non_existant_group(self):
        '''cannot remove a username of a group who is not in the directory'''
        with self.assertRaises(ValueError):
            groups.remove_member('not_there', 'not_there')

    def test_remove_member_non_existant_member(self):
        '''removing non-existant user just does nothing'''
        groups.remove_member(self.existing_group['name'], 'not_there')


if __name__ == "__main__":
    unittest.main()
