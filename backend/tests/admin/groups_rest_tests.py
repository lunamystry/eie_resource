"""
Until I figure out how to setup an tear down, these are manual tests.
You much know what is in the database
"""
import unittest
import backend


class GroupsRestTestCase(unittest.TestCase):

    def setUp(self):
        backend.app.config['TESTING'] = True
        self.app = backend.app.test_client()

    def test_get_groups(self):
        """ I want to be able to get all groups, assuming database works """
        rv = self.app.get("/groups")
        print rv.data

    def test_get_group_members(self):
        """ I should be able to get group members """
        rv = self.app.get("/groups/natsuki")
        print rv.data

    def test_create_group_members(self):
        """ I should be able to add a member to a group """
        rv = self.app.post("/groups/natsuki",
                           content_type="application/json",
                           data='{"username":"guneap"}')
        print rv.data

    def test_get_group_member(self):
        """ I should be able to add a member to a group """
        rv = self.app.get("/groups/natsuki/guneap")
        print rv.data

    def test_delete_group_member(self):
        """ I should be able to add a member to a group """
        rv = self.app.delete("/groups/natsuki/guneap")
        print rv.data


if __name__ == "__main__":
    unittest.main()
