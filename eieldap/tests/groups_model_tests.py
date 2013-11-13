from mock import patch, Mock
from eieldap.manager import Manager
from eieldap import models
import unittest
import tempfile


@patch('eieldap.manager.Manager')
class GroupsTestCase(unittest.TestCase):
    def test_save(self, mock_Manager):
        """ Create a new group or update existing one """
        manager = mock_Manager.return_value

        # exists
        manager.find_one.return_value = {"name": "Testing"}
        group = models.Groups(manager)
        self.assertTrue(group.save({"name":"Testing"}))

        # Does not exist
        manager.find_one.return_value = None
        self.assertTrue(group.save({"name":"Testing"}))
        self.assertTrue(manager.create.assert_called())

        # what if I pass in Group members for giggles
        members = ['leny']
        self.assertTrue(group.save({"name":"Testing"}))

    def test_delete(self, mock_Manager):
        """ Should check first if the thing exists before it deletes it"""
        manager = mock_Manager.return_value
        manager.find_one.return_value = {"name": "Testing"}
        group = models.Groups(manager)
        group.delete("Testing")

        self.assertTrue(manager.find_one.assert_called())
        self.assertTrue(manager.delete.assert_called())

    def test_find_one(self, mock_Manager):
        """ Should be able to use the name of the group"""
        members = ['mandla', 'leny']
        return_attr = {"cn":"natsuki", "dn":"id", "member": members}
        expected_attr = {"name":"natsuki", "id":"id", "members": members}

        manager = mock_Manager.return_value
        manager.find_one.return_value = return_attr
        manager.find_by_dn.return_value = return_attr

        # Can find one by just the name
        group = models.Groups(manager).find_one("natsuki")
        self.assertEquals(group, expected_attr)

        # Can find one by attributes
        group = models.Groups(manager).find_one(attr=expected_attr)
        self.assertEquals(group, expected_attr)

        # what if both the name and attr are given
        ignored_attr["name"] = "magrat"
        group = models.Groups(manager).find_one(name="natsuki",
                                                attr=ignored_attr)
        self.assertEquals(group, expected_attr)

        # what if both are None
        group = models.Groups(manager).find_one(name=None, attr=None)
        self.assertEquals(group, None)

    def test_find(self, mock_Manager):
        """ Give me back all the groups """
        groups = models.Groups().find()

if __name__ == "__main__":
    unittest.main()
