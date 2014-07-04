import unittest
import read


class dhcp_parse_testcase(unittest.TestCase):
    def test_strip_comments(self):
        lines = ["this line # has a comment",
                 "this line does not have a comment",
                 "# this line starts with a comment"]
        expected = ["this line ",
                    "this line does not have a comment",
                    ""]

        result = read.strip_comments(lines)
        self.assertEquals(expected, result)

    def test_options_multiple_values(self):
        lines = ["option multi-values 1,2, 2,3, 4;"]
        expected = {'multi-values': ['1', '2', '2', '3', '4']}

        result = read.read_options(lines)
        self.assertEquals(expected, result)

    def test_options_single_value(self):
        lines = ["option single-value 1;"]
        expected = {'single-value': ['1']}

        result = read.read_options(lines)
        self.assertEquals(expected, result)

    def test_options_indented_line(self):
        lines = ["        option indented 1,2, 2,3,4;"]
        expected = {'indented': ['1', '2', '2', '3', '4']}

        result = read.read_options(lines)
        self.assertEquals(expected, result)

    def test_options_not_option(self):
        lines = ["not-option"]
        expected = {}

        result = read.read_options(lines)
        self.assertEquals(expected, result)

    def test_read_parameters(self):
        ''' Not exhaustive test of parameter extraction'''
        lines = ['authoritative;',
                 'unknown bugger this is;',
                 'server-duid LLT duid;']

        expected = {'authoritative': '',
                    'server-duid LLT': 'duid'}

        result = read.read_parameters(lines)
        self.assertEquals(expected, result)

    def test_read_parameters_indented(self):
        ''' Not exhaustive test of parameter extraction'''
        lines = ['     authoritative;',
                 '      unknown bugger this is;',
                 '   server-duid LLT duid;']

        expected = {'authoritative': '',
                    'server-duid LLT': 'duid'}

        result = read.read_parameters(lines)
        self.assertEquals(expected, result)

    def test_read_adi(self):
        lines = ["deny;",
                 "allow fenix;",
                 "allow bar;",
                 "deny boo;",
                 "ignore baz;"]
        expected = [{'allow': 'fenix'},
                    {'allow': 'bar'},
                    {'deny': 'boo'},
                    {'ignore': 'baz'}]

        result = read.read_adi(lines)
        self.assertEquals(expected, result)

    def test_read_groups(self):
        lines = ['ddns-update-style none;\n',
                 'authoritative;\n',
                 'option domain-name "eg.org"\n',
                 'option domain-name-servers ns1.eg.org, ns2.eg.org\n',
                 '\n',
                 '\n',
                 'subnet 172.16.31.0 netmask 255.255.255.0 {\n',
                 '    # default gateway\n',
                 '    option routers 172.16.31.10;\n',
                 '    option subnet-mask 255.255.255.0;\n',
                 '\n',
                 '    option domain-name "aaaaaa";\n',
                 '    option domain-name-servers 172.16.31.10;\n',
                 '    #option nis-domain "domain.org";\n',
                 '\n',
                 '    range dynamic-bootp 172.16.31.80 172.16.31.90;\n',
                 '    default-lease-time 21600;\n',
                 '    max-lease-time 43200;\n',
                 '\n',
                 '    host test {\n',
                 '        hardware ethernet 00:23:8b:42:3f:d1;\n',
                 '        fixed-address 172.16.31.3;\n',
                 '    }\n',
                 '}\n',
                 '\n',
                 'host test3 {\n',
                 '    hardware ethernet 00:23:8b:42:3f:d1;\n',
                 '    fixed-address 192.129.74.2;\n',
                 '}\n',
                 '\n',
                 'host test4 {\n',
                 '    hardware ethernet 00:23:8b:42:3f:d1;\n',
                 '    fixed-address 192.129.74.2;\n',
                 '}\n']
        expected = [{'name': 'subnet 172.16.31.0 netmask 255.255.255.0 ',
                     'groups': [{'groups': [],
                                 'name': 'host test ',
                                 'parameters': {'hardware': 'ethernet 00:23:8b:42:3f:d1',
                                                'fixed-address': '172.16.31.3'},
                                 'options': {}}],
                     'parameters': {'default-lease-time': '21600',
                                    'max-lease-time': '43200'},
                     'options': {'domain-name': ['"aaaaaa"'],
                                 'routers': ['172.16.31.10'],
                                 'subnet-mask': ['255.255.255.0'],
                                 'domain-name-servers': ['172.16.31.10'],
                                 'nis-domain': ['"domain.org"']}},
                    {'name': 'host test3 ',
                     'groups': [],
                     'parameters': {'hardware': 'ethernet 00:23:8b:42:3f:d1',
                                    'fixed-address': '192.129.74.2'},
                     'options': {}},
                    {'name': 'host test4 ',
                     'groups': [],
                     'parameters': {'hardware': 'ethernet 00:23:8b:42:3f:d1',
                                    'fixed-address': '192.129.74.2'},
                     'options': {}}
                    ]
        self.maxDiff = None
        result = read.read_groups(lines)
        self.assertEquals(expected, result)
