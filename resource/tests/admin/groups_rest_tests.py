"""
Until I figure out how to setup an tear down, these are manual tests.
You much know what is in the database
"""
import unittest
import resource


class GroupsRestTestCase(unittest.TestCase):

    def setUp(self):
        resource.app.config['TESTING'] = True
        self.app = resource.app.test_client()

    def test_get_groups(self):
        """ I want to be able to get all groups, assuming database works """
        rv = self.app.get("/groups")
        # print rv.data

    def test_get_group_members(self):
        """ I should be able to get group members """
        rv = self.app.get("/groups/natsuki")
        # print rv.data

    def test_create_group_members(self):
        """ I should be able to get group members """
        rv = self.app.post("/groups/natsuki",
                           content_type="application/json",
                           data='{"name":"Natsuki"}')
        print rv.data

if __name__ == "__main__":
    unittest.main()
