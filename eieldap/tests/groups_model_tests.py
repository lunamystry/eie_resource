from mock import patch, Mock
from eieldap import models
import unittest


class GroupsTestCase(unittest.TestCase):
    def test_save(self):
        """ Create a new group or update existing one """
        group_to_save = {"name": "natsuki", "members": ['mandla', 'leny']}
        expected_group = {"name": "natsuki", "members": ['mandla', 'leny']}
        ignored_group = {"name": "natsuki", "members": ['mandla', 'leny']}
        invalid_group = {"name": "navina"}

        # can't create without atleast one member
        with self.assertRaises(TypeError):
            models.Groups.save(invalid_group)

        # Does not exist
        self.assertTrue(models.Groups.save(group_to_save))

        # exists
        group_to_save = {"name": "natsuki", "members": ['mandla', 'leonard']}
        expected_group = {"name": "natsuki", "members": ['mandla', 'leonard']}
        self.assertTrue(models.Groups.save(group_to_save))
        group = models.Groups.find_one("natsuki")
        self.assertEquals(group, expected_group)

    def test_delete(self):
        """ Should check first if the thing exists before it deletes it"""
        group_to_save = {"name": "Testing", "members": ['mandla', 'leny']}
        expected_group = {"name": "Testing", "members": ['mandla', 'leny']}
        group = models.Groups.find_one("Testing")
        if group:
            models.Groups.delete(group['name'])
        models.Groups.save(group_to_save)
        group = models.Groups.find_one("Testing")
        self.assertEquals(group, expected_group)

        models.Groups.delete("Testing")
        group = models.Groups.find_one("Testing")
        self.assertEquals(group, None)

        #  should be able to delete using a group
        group_to_save = {"name": "Testing", "members": ['mandla', 'leny']}
        models.Groups.save(group_to_save)
        group = models.Groups.find_one("Testing")
        self.assertEquals(group, expected_group)
        models.Groups.delete(group=group_to_save)
        group = models.Groups.find_one("Testing")
        self.assertEquals(group, None)

    def test_find_one(self):
        """ Should be able to use the name of the group"""
        group_to_save = {"name": "natsuki", "members": ['mandla', 'leny']}
        expected_group = {"name": "natsuki", "members": ['mandla', 'leny']}
        ignored_group = {"name": "natsuki", "members": ['mandla', 'leny']}
        invalid_group = {"name": "navina"}

        # None if group does not exist
        group = models.Groups.find_one("qpoipwoqi")
        self.assertEquals(group, None)

        # Can find one by just the name
        group = models.Groups.find_one("natsuki")
        if group:
            models.Groups.delete(group['name'])
        models.Groups.save(group_to_save)
        group = models.Groups.find_one("natsuki")
        self.assertEquals(group, expected_group)

        # Can find one by attributes
        group = models.Groups.find_one(attr=expected_group)
        self.assertEquals(group, expected_group)

        group = models.Groups.find_one(attr=invalid_group)
        self.assertNotEquals(group, expected_group)

        # what if both the name and attr are given
        ignored_group["name"] = "magrat"
        group = models.Groups.find_one(name="natsuki",
                                                attr=ignored_group)
        self.assertEquals(group, expected_group)

        # what if both are None
        group = models.Groups.find_one(name=None, attr=None)
        self.assertEquals(group, None)

    def test_add_group_member(self):
        """ Can I add a group member?"""
        original_group = {"name": "natsuki", "members": ['mandla', 'leny']}
        expected_group = {"name": "natsuki", "members": ['mandla', 'leny', 'leonard']}
        already_member = "mandla"
        existing_user = "leonard"
        non_existing_user = "poiqaalkj"

        # add to a group that exists
        models.Groups.add_member("natsuki", existing_user)
        group = models.Groups.find_one("natsuki")
        self.assertEquals(group, expected_group)

        # models.Groups.add_member("natsuki", already_member)
        group = models.Groups.find_one("natsuki")
        self.assertEquals(group, expected_group)

        with self.assertRaises(ValueError):
            models.Groups.add_member("natsuki", non_existing_user)

        # add to a group that does not exist
        with self.assertRaises(ValueError):
            models.Groups.add_member("aslkjalskj", existing_user)
        with self.assertRaises(ValueError):
            models.Groups.add_member("aslkjqoi", non_existing_user)
        with self.assertRaises(ValueError):
            models.Groups.add_member("alskjaslkj", non_existing_user)


if __name__ == "__main__":
    unittest.main()
