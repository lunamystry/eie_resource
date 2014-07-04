import unittest
import read as dp


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
        lines = ["option multi-values 1,2, 2,3, 4;"]
        expected = {'multi-values': ['1', '2', '2', '3', '4']}

        result = dp.read_options(lines)
        self.assertEquals(expected, result)

    def test_options_single_value(self):
        lines = ["option single-value 1;"]
        expected = {'single-value': ['1']}

        result = dp.read_options(lines)
        self.assertEquals(expected, result)

    def test_options_indented_line(self):
        lines = ["        option indented 1,2, 2,3,4;"]
        expected = {'indented': ['1', '2', '2', '3', '4']}

        result = dp.read_options(lines)
        self.assertEquals(expected, result)

    def test_options_not_option(self):
        lines = ["not-option"]
        expected = {}

        result = dp.read_options(lines)
        self.assertEquals(expected, result)

    def test_read_parameters(self):
        ''' Not exhaustive test of parameter extraction'''
        lines = ['authoritative;',
                 'unknown bugger this is;',
                 'server-duid LLT duid;']

        expected = {'authoritative': '',
                    'server-duid LLT': 'duid'}

        result = dp.read_parameters(lines)
        self.assertEquals(expected, result)

    def test_read_parameters_indented(self):
        ''' Not exhaustive test of parameter extraction'''
        lines = ['     authoritative;',
                 '      unknown bugger this is;',
                 '   server-duid LLT duid;']

        expected = {'authoritative': '',
                    'server-duid LLT': 'duid'}

        result = dp.read_parameters(lines)
        self.assertEquals(expected, result)
