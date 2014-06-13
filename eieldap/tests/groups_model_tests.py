# from mock import patch, Mock
from eieldap import models
import unittest


class groupsTestCase(unittest.TestCase):

    def setUp(self):
        self.valid = {"name": "natsuki", "members": ['john', 'gary']}
        self.expected = {"name": "natsuki", "members": ['john', 'gary']}
        self.updated_valid = {"name": "natsuki", "members": ['gary', 'vicky']}
        self.expected_updated = {"name": "natsuki",
                                 "members": ['gary', 'vicky']}
        self.invalid = {"name": "navina"}

        self.valid_attr = {'members': self.valid['members']}
        self.invalid_attr = self.invalid
        self.one_invalid_attr = self.valid

    def tearDown(self):
        models.groups.delete(self.valid['name'])
        models.groups.delete(self.expected['name'])
        models.groups.delete(self.updated_valid['name'])
        models.groups.delete(self.expected_updated['name'])

    def test_save_and_find_known_group(self):
        '''can save a group which does not exist and is valid'''
        self.assertTrue(models.groups.save(self.valid))
        group = models.groups.find_one(self.valid['name'])
        self.assertEquals(group, self.valid)

    def test_save_a_group_that_exists(self):
        '''saving a group that exists, will update its members'''
        self.assertTrue(models.groups.save(self.valid))
        group = models.groups.find_one(self.valid['name'])
        self.assertEquals(group, self.expected)
        self.assertTrue(models.groups.save(self.updated_valid))
        self.assertEquals(group, self.updated_valid)

    def test_cant_save_invalid_group(self):
        ''' Because LDAP does not allow creating a group without members, I
        don't allow it either'''
        with self.assertRaises(TypeError):
            models.groups.save(self.invalid)

    def test_delete_an_existing_group(self):
        ''' If a group exists, I should be able to delete it and not get it
        back '''
        self.assertTrue(models.groups.save(self.valid))
        models.groups.delete(self.valid['name'])
        group = models.groups.find_one(self.valid['name'])
        self.assertEquals(group, None)

    def test_delete_a_non_existing_group(self):
        ''' If a group does not exist, it does not matter, just pretend it was
        deleted'''
        models.groups.delete(self.valid['name'])
        group = models.groups.find_one(self.valid['name'])
        self.assertEquals(group, None)

    def test_find_using_valid_attribute(self):
        self.assertTrue(models.groups.save(self.valid))
        group = models.groups.find_one(attr=self.valid_attr)
        self.assertEquals(group, self.valid)

    def test_find_using_one_invalid_attribute(self):
        '''I should still get back a group that matches the other attributes'''
        self.assertTrue(models.groups.save(self.valid))
        group = models.groups.find_one(attr=self.one_invalid_attr)
        self.assertEquals(group, self.valid)

    def test_find_a_non_existing_group(self):
        '''If a group does not exist, then None should be returned'''
        group = models.groups.find_one("qpoipwoqi")
        self.assertEquals(group, None)

    def test_find_can_specify_both_name_and_attr_name_valid(self):
        '''will return one group if name is valid'''
        self.assertTrue(models.groups.save(self.valid))
        group = models.groups.find_one(name=self.valid['name'],
                                       group=self.invalid_attr)
        self.assertEquals(group, self.expected)

    def test_find_can_specify_both_name_and_attr_attributes_valid(self):
        '''will return one group if attributes are valid'''
        self.assertTrue(models.groups.save(self.valid))
        group = models.groups.find_one(name='aslkajsa',
                                       attr=self.valid_attr)
        self.assertEquals(group, self.valid)

    def test_find_none_if_both_name_and_attr_are_not_given(self):
        '''If you a name or attribute are None, then None is returned'''
        group = models.groups.find_one(name=None, attr=None)
        self.assertEquals(group, None)


# class groupMembersTestCase(unittest.TestCase):
# 
#     def setUp(self):
#         self.original_group = {"name": "testgroup", "members": ['guneap']}

    # def test_add_group_member(self):
    #     """ Can I add a group member?"""
    #     guneap = {"username": "guneap",
    #               "first_name": "Gunea",
    #               "last_name": "Pig",
    #               "email": "123@students.wits.ac.za",
    #               "password": "secret",
    #               "yos": "3"}
    #     mandla = {"username": "mandla",
    #               "first_name": "Mandla",
    #               "last_name": "Niigata",
    #               "email": "mandla.niigata@students.wits.ac.za",
    #               "password": "passing",
    #               "yos": "4"}
    #     already_member = "mandla"
    #     existing_user = "guneap"
    #     new_member = "guneap"
    #     non_existing_user = "poiqaalkj"

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

    #     # add to a group that exists
    #     models.groups.add_member("natsuki", new_member)
    #     group = models.groups.find_one("natsuki")
    #     expected = {"name": "natsuki", "members": ['mandla', 'guneap']}
    #     self.assertEquals(group, expected)
    #     models.groups.remove_member("natsuki", new_member)

    #     models.groups.add_member("natsuki", already_member)
    #     group = models.groups.find_one("natsuki")
    #     original_group = {"name": "natsuki", "members": ['mandla']}
    #     self.assertEquals(group, original_group)

    #     with self.assertRaises(ValueError):
    #         models.groups.add_member("natsuki", non_existing_user)

    #     # add to a group that does not exist
    #     with self.assertRaises(ValueError):
    #         models.groups.add_member("aslkjalskj", existing_user)
    #     with self.assertRaises(ValueError):
    #         models.groups.add_member("aslkjqoi", non_existing_user)
    #     with self.assertRaises(ValueError):
    #         models.groups.add_member("alskjaslkj", non_existing_user)

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
    #     models.groups.add_member("natsuki", existing_user)
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
