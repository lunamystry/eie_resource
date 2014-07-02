import unittest
import dhcp_parse as dp


class CommentsTests(unittest.TestCase):
    def test_strip_comments(self):
        lines = ["this line # has a comment",
                 "this line does not have a comment",
                 "# this line starts with a comment"]
        expected = ["this line ",
                    "this line does not have a comment",
                    ""]

        result = dp.strip_comments(lines)
        self.assertEquals(expected, result)
