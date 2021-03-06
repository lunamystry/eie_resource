from __future__ import unicode_literals
from __future__ import print_function

import unittest
import json
import backend


class BackendRestTestCase(unittest.TestCase):

    def setUp(self):
        backend.app.config['TESTING'] = True
        self.app = backend.app.test_client()

    def test_get_bookings(self):
        rv = self.app.get("/bookings")
        print(rv.data)

    def test_post_booking(self):
        """ I should be able to add a member to a group """
        data = ('{"date": "2014-11-20 14H00",'
                '"duration": "20",'  # minutes
                '"computers": [1,2,3],'
                '"software": ["python"],'
                '"demis": [{"name": "student"}],'
                '"contact_person": "name"}')
        rv = self.app.post("/bookings",
                           content_type="application/json",
                           data=data)
        self.assertEquals(json.loads(rv.data), [])

if __name__ == "__main__":
    unittest.main()
