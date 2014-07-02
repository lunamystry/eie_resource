import unittest
import dhcp_parse as dp


class dhcp_parse_testcase(unittest.TestCase):
    def test_strip_comments(self):
        lines = ["this line # has a comment",
                 "this line does not have a comment",
                 "# this line starts with a comment"]
        expected = ["this line ",
                    "this line does not have a comment",
                    ""]

        result = dp.strip_comments(lines)
        self.assertEquals(expected, result)

    def test_options_multiple_values(self):
        lines = ["option multi-values 1,2, 2,3, 4"]
        expected = [{'name': 'multi-values',
                     'values': ['1', '2', '2', '3', '4']}]

        result = dp.options(lines)
        self.assertEquals(expected, result)

    def test_options_single_value(self):
        lines = ["option single-value 1"]
        expected = [{'name': 'single-value',
                     'values': ['1']}]

        result = dp.options(lines)
        self.assertEquals(expected, result)

    def test_options_indented_line(self):
        lines = ["        option indented 1,2, 2,3,4"]
        expected = [{'name': 'indented',
                     'values': ['1', '2', '2', '3', '4']}]

        result = dp.options(lines)
        self.assertEquals(expected, result)

    def test_options_not_option(self):
        lines = ["not-option"]
        expected = []

        result = dp.options(lines)
        self.assertEquals(expected, result)