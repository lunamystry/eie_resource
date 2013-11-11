from mock import patch, Mock
import unittest
from eieldap import models
import tempfile


@patch('models.Manager')
class GroupsTestCase(unittest.TestCase):
    def test_save(self, Manager):
        """ Create a new group """
        manager = Manager.return_value
        manager.find_one.return_value = {"group": "name"}
        group = models.Groups()
        self.assertTrue(group.save({"name":"Testing"}))
        manager.find_one.return_value = None
        self.assertTrue(group.save({"name":"Testing"}))
        self.assertTrue(manager.create.assert_called())

    def test_update(self, manager):
        """ Can I update a group? I hope so"""
        pass

if __name__ == "__main__":
    unittest.main()
