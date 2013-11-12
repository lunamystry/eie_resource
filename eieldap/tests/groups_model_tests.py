from mock import patch, Mock
import unittest
from eieldap import models
import tempfile


@patch('models.Manager')
class GroupsTestCase(unittest.TestCase):
    def test_save(self, Manager):
        """ Create a new group or update existing one """
        manager = Manager.return_value

        # exists
        manager.find_one.return_value = {"name": "Testing"}
        group = models.Groups()
        self.assertTrue(group.save({"name":"Testing"}))

        # Does not exist
        manager.find_one.return_value = None
        self.assertTrue(group.save({"name":"Testing"}))
        self.assertTrue(manager.create.assert_called())

    def test_update(self, Manager):
        """ Can I update a group? I hope so"""
        pass

    def test_delete(self, Manager):
        """ Should check first if the thing exists before it deletes it"""
        manager = Manager.return_value
        manager.find_one.return_value = {"name": "Testing"}
        group = models.Groups()
        group.delete("Testing")
        # This does not work
        self.assertTrue(manager.find_one.assert_called())
        self.assertTrue(manager.delete.assert_called())


if __name__ == "__main__":
    unittest.main()
