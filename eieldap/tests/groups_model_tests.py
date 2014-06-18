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
    #     models.groups.delete(self.valid['name'])
    #     models.groups.delete(self.expected['name'])
    #     models.groups.delete(self.updated_valid['name'])

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

    # def test_delete_an_existing_group(self):
    #     ''' If a group exists, I should be able to delete it and not get it
    #     back '''
    #     self.assertTrue(models.groups.save(self.valid))
    #     models.groups.delete(self.valid['name'])
    #     group = models.groups.find_one(self.valid['name'])
    #     self.assertEquals(group, None)

    # def test_delete_a_non_existing_group(self):
    #     ''' If a group does not exist, it does not matter, just pretend it was
    #     deleted'''
    #     models.groups.delete(self.valid['name'])
    #     group = models.groups.find_one(self.valid['name'])
    #     self.assertEquals(group, None)

    # def test_find_using_valid_group(self):
    #     self.assertTrue(models.groups.save(self.valid))
    #     group = models.groups.find_one(group=self.valid)
    #     self.assertEquals(group, self.valid)

    # def test_find_a_non_existing_group(self):
    #     '''If a group does not exist, then None should be returned'''
    #     group = models.groups.find_one("qpoipwoqi")
    #     self.assertEquals(group, None)

    # def test_find_can_specify_both_name_and_group(self):
    #     '''should use names if both name and group are given'''
    #     self.assertTrue(models.groups.save(self.valid))
    #     group = models.groups.find_one(name=self.valid['name'],
    #                                    group=self.no_members)
    #     self.assertEquals(group, self.expected)

    # def test_find_can_specify_wrong_name_and_correct_group(self):
    #     '''will return one group if attributes are valid'''
    #     self.assertTrue(models.groups.save(self.valid))
    #     group = models.groups.find_one(name='aslkajsa',
    #                                    group=self.valid)
    #     self.assertEquals(group, self.valid)

    # def test_find_None_if_both_name_and_group_are_None(self):
    #     '''If you a name or attribute are None, then None is returned'''
    #     group = models.groups.find_one(name=None, group=None)
    #     self.assertEquals(group, None)


class groupMembersTestCase(unittest.TestCase):
    pass
    # def setUp(self):
    #     self.existing_user = {"username": "guneap",
    #                           "first_name": "Gunea",
    #                           "last_name": "Pig",
    #                           "email": "123@students.wits.ac.za",
    #                           "password": "secret",
    #                           "hosts": ['babbage.ug.eie.wits.ac.za'],
    #                           "yos": "3"}
    #     self.existing_group = {"name": "testgroup",
    #                            "members": [self.existing_user['username']]}
    #     self.non_existing_user = "poiqaalkj"
    #     models.users.save(self.existing_user)
    #     models.groups.save(self.existing_group)
    #     self.new_member = {"username": "johnd",
    #                        "first_name": "John",
    #                        "last_name": "Doe",
    #                        "email": "mandla.niigata@students.wits.ac.za",
    #                        "password": "passing",
    #                        "hosts": ['dummy'],
    #                        "yos": "4"}

    # def tearDown(self):
    #     models.users.delete(self.existing_user['name'])
    #     models.groups.delete(self.existing_group['name'])

    # def test_save_member_new_member(self):
    #     '''I should be able to simply save a new valid member'''
    #     models.groups.save_member(self.existing_group['name'],
    #                              self.new_member['username'])

    # def test_save_group_member(self):
    #     """ Can I save a group member?"""

    #     # remove from a group that exists
    #     user = models.users.find_one("guneap")
    #     if user:
    #         models.users.delete("guneap")
    #     models.users.save(guneap)
    #     user = models.users.find_one("mandla")
    #     if user:
    #         models.users.delete("mandla")
    #     models.users.save(mandla)

    #     group = models.groups.find_one("natsuki")
    #     if group:
    #         models.groups.delete("natsuki")
    #     models.groups.save(original_group)

    #     # save to a group that exists
    #     models.groups.save_member("natsuki", new_member)
    #     group = models.groups.find_one("natsuki")
    #     expected = {"name": "natsuki", "members": ['mandla', 'guneap']}
    #     self.assertEquals(group, expected)
    #     models.groups.remove_member("natsuki", new_member)

    #     models.groups.save_member("natsuki", already_member)
    #     group = models.groups.find_one("natsuki")
    #     original_group = {"name": "natsuki", "members": ['mandla']}
    #     self.assertEquals(group, original_group)

    #     with self.assertRaises(ValueError):
    #         models.groups.save_member("natsuki", non_existing_user)

    #     # save to a group that does not exist
    #     with self.assertRaises(ValueError):
    #         models.groups.save_member("aslkjalskj", existing_user)
    #     with self.assertRaises(ValueError):
    #         models.groups.save_member("aslkjqoi", non_existing_user)
    #     with self.assertRaises(ValueError):
    #         models.groups.save_member("alskjaslkj", non_existing_user)

    # def test_remove_group_member(self):
    #     """ Can I remove a group member?"""
    #     original_group = {"name": "natsuki", "members": ['mandla']}
    #     expected = {"name": "natsuki", "members": ['mandla', 'guneap']}
    #     guneap = {"username": "guneap",
    #               "first_name": "Gunea",
    #               "last_name": "Pig",
    #               "email": "123@students.wits.ac.za",
    #               "password": "secret",
    #               "yos": "3"}
    #     already_member = "mandla"
    #     existing_user = "guneap"
    #     non_existing_user = "poiqaalkj"

    #     # remove from a group that exists
    #     user = models.users.find_one("guneap")
    #     if user:
    #         models.users.delete("guneap")
    #     models.users.save(guneap)

    #     group = models.groups.find_one("natsuki")
    #     if group:
    #         models.groups.delete("natsuki")
    #     models.groups.save(original_group)

    #     # Add a member
    #     models.groups.save_member("natsuki", existing_user)
    #     group = models.groups.find_one("natsuki")
    #     new_group = {"name": "natsuki", "members": ['mandla', 'guneap']}
    #     self.assertEquals(group, new_group)
    #     # remove the member
    #     models.groups.remove_member("natsuki", existing_user)
    #     group = models.groups.find_one("natsuki")
    #     original_group = {"name": "natsuki", "members": ['mandla']}
    #     self.assertEquals(group, original_group)

    #     # member does not exist, I don't care, remain the same
    #     models.groups.remove_member("natsuki", non_existing_user)
    #     group = models.groups.find_one("natsuki")
    #     original_group = {"name": "natsuki", "members": ['mandla']}
    #     self.assertEquals(group, original_group)

    #     # remove from a group that does not exist
    #     with self.assertRaises(ValueError):
    #         models.groups.remove_member("aslkjalskj", existing_user)
    #     with self.assertRaises(ValueError):
    #         models.groups.remove_member("aslkjqoi", non_existing_user)
    #     with self.assertRaises(ValueError):
    #         models.groups.remove_member("alskjaslkj", non_existing_user)

    #     # what if there is only one member remaining
    #     with self.assertRaises(ReferenceError):
    #         models.groups.remove_member("natsuki", "mandla")


if __name__ == "__main__":
    unittest.main()
