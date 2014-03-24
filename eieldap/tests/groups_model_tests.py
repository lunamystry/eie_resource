from mock import patch, Mock
from eieldap import models
import unittest


class groupsTestCase(unittest.TestCase):
    def test_save(self):
        """ Create a new group or update existing one """
        group_to_save = {"name": "natsuki", "members": ['mandla', 'leny']}
        expected_group = {"name": "natsuki", "members": ['mandla', 'leny']}
        ignored_group = {"name": "natsuki", "members": ['mandla', 'leny']}
        invalid_group = {"name": "navina"}

        # can't create without atleast one member
        with self.assertRaises(TypeError):
            models.groups.save(invalid_group)

        # Does not exist
        self.assertTrue(models.groups.save(group_to_save))

        # exists
        group_to_save = {"name": "natsuki", "members": ['mandla', 'leonard']}
        expected_group = {"name": "natsuki", "members": ['mandla', 'leonard']}
        self.assertTrue(models.groups.save(group_to_save))
        group = models.groups.find_one("natsuki")
        self.assertEquals(group, expected_group)

    def test_delete(self):
        """ Should check first if the thing exists before it deletes it"""
        group_to_save = {"name": "Testing", "members": ['mandla', 'leny']}
        expected_group = {"name": "Testing", "members": ['mandla', 'leny']}
        group = models.groups.find_one("Testing")
        if group:
            models.groups.delete(group['name'])
        models.groups.save(group_to_save)
        group = models.groups.find_one("Testing")
        self.assertEquals(group, expected_group)

        models.groups.delete("Testing")
        group = models.groups.find_one("Testing")
        self.assertEquals(group, None)

        #  should be able to delete using a group
        group_to_save = {"name": "Testing", "members": ['mandla', 'leny']}
        models.groups.save(group_to_save)
        group = models.groups.find_one("Testing")
        self.assertEquals(group, expected_group)
        models.groups.delete(group=group_to_save)
        group = models.groups.find_one("Testing")
        self.assertEquals(group, None)

    def test_find_one(self):
        """ Should be able to use the name of the group"""
        group_to_save = {"name": "natsuki", "members": ['mandla', 'leny']}
        expected_group = {"name": "natsuki", "members": ['mandla', 'leny']}
        ignored_group = {"name": "natsuki", "members": ['mandla', 'leny']}
        invalid_group = {"name": "navina"}

        # None if group does not exist
        group = models.groups.find_one("qpoipwoqi")
        self.assertEquals(group, None)

        # Can find one by just the name
        group = models.groups.find_one("natsuki")
        if group:
            models.groups.delete(group['name'])
        models.groups.save(group_to_save)
        group = models.groups.find_one("natsuki")
        self.assertEquals(group, expected_group)

        # Can find one by attributes
        group = models.groups.find_one(attr=expected_group)
        self.assertEquals(group, expected_group)

        group = models.groups.find_one(attr=invalid_group)
        self.assertNotEquals(group, expected_group)

        # what if both the name and attr are given
        ignored_group["name"] = "magrat"
        group = models.groups.find_one(name="natsuki",
                                                attr=ignored_group)
        self.assertEquals(group, expected_group)

        # what if both are None
        group = models.groups.find_one(name=None, attr=None)
        self.assertEquals(group, None)

    def test_add_group_member(self):
        """ Can I add a group member?"""
        original_group = {"name": "natsuki", "members": ['mandla']}
        guneap = {"username": "guneap",
                  "first_name": "Gunea",
                  "last_name": "Pig",
                  "email": "123@students.wits.ac.za",
                  "password": "secret",
                  "yos": "3"}
        mandla = {"username": "mandla",
                  "first_name": "Mandla",
                  "last_name": "Niigata",
                  "email": "mandla.niigata@students.wits.ac.za",
                  "password": "passing",
                  "yos": "4"}
        already_member = "mandla"
        existing_user = "guneap"
        new_member = "guneap"
        non_existing_user = "poiqaalkj"

        # remove from a group that exists
        user = models.users.find_one("guneap")
        if user:
            models.users.delete("guneap")
        models.users.save(guneap)
        user = models.users.find_one("mandla")
        if user:
            models.users.delete("mandla")
        models.users.save(mandla)

        group = models.groups.find_one("natsuki")
        if group:
            models.groups.delete("natsuki")
        models.groups.save(original_group)

        # add to a group that exists
        models.groups.add_member("natsuki", new_member)
        group = models.groups.find_one("natsuki")
        expected_group = {"name": "natsuki", "members": ['mandla', 'guneap']}
        self.assertEquals(group, expected_group)
        models.groups.remove_member("natsuki", new_member)

        models.groups.add_member("natsuki", already_member)
        group = models.groups.find_one("natsuki")
        original_group = {"name": "natsuki", "members": ['mandla']}
        self.assertEquals(group, original_group)

        with self.assertRaises(ValueError):
            models.groups.add_member("natsuki", non_existing_user)

        # add to a group that does not exist
        with self.assertRaises(ValueError):
            models.groups.add_member("aslkjalskj", existing_user)
        with self.assertRaises(ValueError):
            models.groups.add_member("aslkjqoi", non_existing_user)
        with self.assertRaises(ValueError):
            models.groups.add_member("alskjaslkj", non_existing_user)

    def test_remove_group_member(self):
        """ Can I remove a group member?"""
        original_group = {"name": "natsuki", "members": ['mandla']}
        expected_group = {"name": "natsuki", "members": ['mandla', 'guneap']}
        guneap = {"username": "guneap",
                  "first_name": "Gunea",
                  "last_name": "Pig",
                  "email": "123@students.wits.ac.za",
                  "password": "secret",
                  "yos": "3"}
        already_member = "mandla"
        existing_user = "guneap"
        non_existing_user = "poiqaalkj"

        # remove from a group that exists
        user = models.users.find_one("guneap")
        if user:
            models.users.delete("guneap")
        models.users.save(guneap)

        group = models.groups.find_one("natsuki")
        if group:
            models.groups.delete("natsuki")
        models.groups.save(original_group)

        # Add a member
        models.groups.add_member("natsuki", existing_user)
        group = models.groups.find_one("natsuki")
        new_group = {"name": "natsuki", "members": ['mandla', 'guneap']}
        self.assertEquals(group, new_group)
        # remove the member
        models.groups.remove_member("natsuki", existing_user)
        group = models.groups.find_one("natsuki")
        original_group = {"name": "natsuki", "members": ['mandla']}
        self.assertEquals(group, original_group)

        # member does not exist, I don't care, remain the same
        models.groups.remove_member("natsuki", non_existing_user)
        group = models.groups.find_one("natsuki")
        original_group = {"name": "natsuki", "members": ['mandla']}
        self.assertEquals(group, original_group)

        # remove from a group that does not exist
        with self.assertRaises(ValueError):
            models.groups.remove_member("aslkjalskj", existing_user)
        with self.assertRaises(ValueError):
            models.groups.remove_member("aslkjqoi", non_existing_user)
        with self.assertRaises(ValueError):
            models.groups.remove_member("alskjaslkj", non_existing_user)

        # what if there is only one member remaining
        with self.assertRaises(ReferenceError):
            models.groups.remove_member("natsuki", "mandla")


    def test_find(self):
        "should return usernames"
        for group in models.groups.find():
            print(group)


if __name__ == "__main__":
    unittest.main()
