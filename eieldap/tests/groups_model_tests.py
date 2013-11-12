from mock import patch, Mock
from eieldap.manager import Manager
from eieldap import models
import unittest
import tempfile

class GroupsTestCase(unittest.TestCase):
#     def test_save(self, Manager):
#         """ Create a new group or update existing one """
#         manager = Manager.return_value

#         # exists
#         manager.find_one.return_value = {"name": "Testing"}
#         group = models.Groups()
#         self.assertTrue(group.save({"name":"Testing"}))

#         # Does not exist
#         manager.find_one.return_value = None
#         self.assertTrue(group.save({"name":"Testing"}))
#         self.assertTrue(manager.create.assert_called())

#     def test_update(self, Manager):
#         """ Can I update a group? I hope so"""
#         pass

#     def test_delete(self, Manager):
#         """ Should check first if the thing exists before it deletes it"""
#         manager = Manager.return_value
#         manager.find_one.return_value = {"name": "Testing"}
#         group = models.Groups()
#         group.delete("Testing")
#         # This does not work
#         self.assertTrue(manager.find_one.assert_called())
#         self.assertTrue(manager.delete.assert_called())

    @patch('eieldap.manager.Manager')
    def test_find_one(self, mock_Manager):
        """ Should be able to use the name of the group"""
        test_attr = {"cn":"natsuki", "dn":"id"}
        expected_attr = {"name":"natsuki", "id":"id"}

        manager = mock_Manager.return_value
        manager.find_one.return_value = test_attr
        manager.find_by_dn.return_value = test_attr

        # Can find one by just the name
        group = models.Groups(manager).find_one("natsuki")
        self.assertEquals(group, expected_attr)

        # Can find one by attributes
        group = models.Groups(manager).find_one(attr=expected_attr)
        self.assertEquals(group, expected_attr)

        # what if both the name and attr are given
        ignored_attr = {"name":"magrat", "id":"id"}
        group = models.Groups(manager).find_one(name="natsuki",
                                                attr=ignored_attr)
        self.assertEquals(group, expected_attr)

        # what if both are None
        group = models.Groups(manager).find_one(name=None, attr=None)
        self.assertEquals(group, None)

if __name__ == "__main__":
    unittest.main()
