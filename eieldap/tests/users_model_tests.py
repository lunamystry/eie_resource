from eieldap import users
import unittest


class UserServicesTests(unittest.TestCase):

    def setUp(self):
        self.valid = {"username": "guneap",
                      "first_name": "Gunea",
                      "last_name": "Pig",
                      "email": ["guneap@students.wits.ac.za"],
                      "password": "passing",
                      "hosts": ['dummy'],
                      "yos": "1"}
        self.invalid = {"username": "testuser"}
        self.existing_user = {"username": "johnd",
                              "first_name": "John",
                              "last_name": "Doe",
                              "email": ["john.doe@students.wits.ac.za"],
                              "password": "passing",
                              "hosts": ['dummy'],
                              "gid_number": "4000",
                              "uid_number": "4001",
                              "login_shell": "/bin/bash",
                              "home_directory": "/home/ug/johnd",
                              "yos": "4"}

    def test_next_uid_number_in_range(self):
        for yos in range(1, 8):
            next_uid = users.next_uid_number(yos)
            start = yos*1000
            end = start + 1000
            self.assertTrue(next_uid in range(start, end))

    def test_next_uid_number_out_of_range(self):
        '''
           1 - first year
           2 - second year
           3 - third year
           4 - fourth year
           5 - postgrad
           6 - staff
           7 - machine
        '''
        with self.assertRaises(ValueError):
            users.next_uid_number(-1)
        with self.assertRaises(ValueError):
            users.next_uid_number(8)

    def test_user_gid_number_in_range(self):
        '''just cause I like more tests'''
        for yos in range(1, 8):
            gid = users.user_gid_number(yos)
            start = yos*1000
            end = start + 1000
            self.assertTrue(gid in range(start, end))

    def test_user_gid_number_out_of_range(self):
        '''look the doc string for test_next_uid_number'''
        with self.assertRaises(ValueError):
            users.user_gid_number(-1)
        with self.assertRaises(ValueError):
            users.user_gid_number(8)

    def test_validate_valid(self):
        users.validate(self.valid)

    def test_validate_invalid(self):
        with self.assertRaises(TypeError):
            users.validate(self.invalid)

    def test_convert_from_ldap(self):
        ldap_attr = {'dn': 'uid=monkeyl,ou=people,dc=eie,dc=wits,dc=ac,dc=za',
                     'displayName': 'Luffy Monkey',
                     'uid': 'monkeyl',
                     'objectClass': ['inetOrgPerson',
                                     'organizationalPerson',
                                     'posixAccount',
                                     'sambaSamAccount',
                                     'hostObject'],
                     'loginShell': '/bin/bash',
                     'userPassword': '{SSHA}qGfneJ66q1r+29LF9AO8jaGnOOi1yz+N',
                     'sambaLMPassword': 'B267DF22CB945E3EAAD3B435B51404EE',
                     'uidNumber': '3000',
                     'gidNumber': '3000',
                     'sambaAcctFlags': '[U         ]',
                     'sambaSID': 'S-1-5-21-3949128619-541665055-2325163404-12000',
                     'sn': 'Monkey',
                     'homeDirectory': '/home/ug/monkeyl',
                     'host': ['babbage.ug.eie.wits.ac.za'],
                     'mail': ['0000000@students.ug.eie.wits.ac.za'],
                     'sambaNTPassword': '36AA83BDCAB3C9FDAF321CA42A31C3FC',
                     'cn': 'Luffy'}
        converted_ldap_attr = {'first_name': 'Luffy',
                               'last_name': 'Monkey',
                               'username': 'monkeyl',
                               'login_shell': '/bin/bash',
                               'uid_number': '3000',
                               'gid_number': '3000',
                               'home_directory': '/home/ug/monkeyl',
                               'hosts': ['babbage.ug.eie.wits.ac.za'],
                               'email': ['0000000@students.ug.eie.wits.ac.za']}
        converted = users.convert(ldap_attr, users.FROM_LDAP_MAP)
        self.assertEquals(converted, converted_ldap_attr)

    def test_convert_to_ldap(self):
        attr = {'username': 'monkeyl',
                'login_shell': '/bin/bash',
                'uid_number': '3000',
                'gid_number': '3000',
                'hosts': ['babbage.ug.eie.wits.ac.za'],
                'last_name': 'Monkey',
                'home_directory': '/home/ug/monkeyl',
                'email': ['320983232@students.ug.eie.wits.ac.za'],
                'first_name': 'Luffy'}
        expected_attr = {'uid': 'monkeyl',
                         'loginShell': '/bin/bash',
                         'uidNumber': '3000',
                         'gidNumber': '3000',
                         'host': ['babbage.ug.eie.wits.ac.za'],
                         'sn': 'Monkey',
                         'homeDirectory': '/home/ug/monkeyl',
                         'mail': ['320983232@students.ug.eie.wits.ac.za'],
                         'cn': 'Luffy'}
        converted = users.convert(attr, users.TO_LDAP_MAP)
        self.assertEquals(converted, expected_attr)

    def test_convert_from_ldap_None(self):
        ''' As long as I can do it I am happy'''
        users.convert(None, users.BASEDN)

    def test_smb_encrypt(self):
        '''As long as it can be called'''
        users.smb_encrypt('password')

    def test_change_password(self):
        '''this just passes things to the manager'''
        users.change_password('user', 'old_password', 'new_password')

    def test_reset_password(self):
        '''this just passes things to the manager'''
        users.reset_password('user')

    # def test_authenticate_valid_credentials(self):
    #     users.authenticate(self.existing_user['username'],
    #                        self.existing_user['password'])

    def test_authenticate_invalid_credentials(self):
        '''this just passes things to the manager'''
        with self.assertRaises(ValueError):
            users.authenticate('invalid_user', 'invalid_password')


class UsersTestCase(unittest.TestCase):

    def setUp(self):
        self.valid = {"username": "guneap",
                      "first_name": "Gunea",
                      "last_name": "Pig",
                      "email": ["guneap@students.wits.ac.za"],
                      "password": "passing",
                      "hosts": ['dummy'],
                      "yos": "1"}
        self.existing_user = {"username": "johnd",
                              "first_name": "John",
                              "last_name": "Doe",
                              "email": ["john.doe@students.wits.ac.za"],
                              "password": "passing",
                              "hosts": ['dummy'],
                              "gid_number": "4000",
                              "uid_number": "4001",
                              "login_shell": "/bin/bash",
                              "home_directory": "/home/ug/johnd",
                              "yos": "4"}
        self.missing_attributes = {"username": "johnd",
                                   "password": "passing",
                                   "hosts": ['dummy'],
                                   "yos": "4"}
        users.delete(self.existing_user['username'])
        users.add(self.existing_user)

    def tearDown(self):
        users.delete(self.existing_user['username'])
        users.delete(self.valid['username'])

    def test_init_user(self):
        valid = {"username": "guneap",
                 "first_name": "Gunea",
                 "last_name": "Pig",
                 "email": ["gunea.pig@students.wits.ac.za"],
                 "password": "passing",
                 "hosts": ['dummy'],
                 "yos": "1"}
        expected_attr = {'cn': 'Gunea',
                         'objectClass': ['inetOrgPerson',
                                         'organizationalPerson',
                                         'posixAccount',
                                         'sambaSamAccount',
                                         'hostObject'],
                         'loginShell': '/bin/bash',
                         'sambaLMPassword': 'F1213CB1AFD3589BAAD3B435B51404EE',
                         'uidNumber': '1000',
                         'sambaAcctFlags': '[U         ]',
                         'gidNumber': '1000',
                         'sambaNTPassword': '6D14A6C43C5C6A2A4B5B45BD97C2F09F',
                         'uid': 'guneap',
                         'displayName': 'Gunea Pig',
                         'host': ['dummy'],
                         'sambaSID': 'S-1-5-21-3949128619-541665055-2325163404-4000',
                         'sn': 'Pig',
                         'homeDirectory': '/home/ug/guneap',
                         'mail': ['gunea.pig@students.wits.ac.za']}
        self.maxDiff = None
        user = users.User(valid)
        del user.attributes['uidNumber']
        del user.attributes['sambaSID']
        del expected_attr['uidNumber']
        del expected_attr['sambaSID']
        self.assertEquals(user.attributes, expected_attr)

    def test_add(self):
        '''simply add a new valid user'''
        users.add(self.valid)

    def test_add_existing(self):
        '''raises an error if the user already exists'''
        with self.assertRaises(ValueError):
            self.assertTrue(users.add(self.existing_user))

    def test_add_missing_required_attributes(self):
        '''adding existing user should update it'''
        with self.assertRaises(TypeError):
            users.add(self.missing_attributes)

    def test_update(self):
        self.existing_user['first_name'] = 'Jane'
        users.update(self.existing_user)
        user = users.find_one(self.existing_user['username'])
        self.existing_user['uid_number'] = '4002'  # This is a problem
        del self.existing_user['password']
        self.assertEquals(user, self.existing_user)

    def test_update_username(self):
        '''you should are not allowed to change username'''
        username = self.existing_user['username']
        self.existing_user['username'] = 'janed'
        users.update(self.existing_user)
        self.existing_user['username'] = username
        user = users.find_one(username)
        del self.existing_user['password']
        self.assertEquals(user, self.existing_user)

    def test_delete(self):
        '''simply delete a user, try to find it and see if its really gone'''
        users.delete(self.existing_user['username'])

    def test_delete_no_username_given(self):
        '''as long as this call does not fail'''
        users.delete(user=self.existing_user)

    def test_delete_nothing_given(self):
        '''as long as this call does not fail'''
        self.assertFalse(users.delete())

    def test_find(self):
        '''as long as it can be called'''
        for user in users.find():
            print(user)

    def test_find_one(self):
        user = users.find_one(self.existing_user['username'])
        del self.existing_user['password']
        self.assertEquals(user, self.existing_user)

    def test_find_one_username_not_given(self):
        user = users.find_one()
        self.assertEquals(user, None)

    def test_add_host(self):
        new_host = "testing.ug.eie.wits.ac.za"
        users.add_host(self.existing_user['username'], new_host)
        user = users.find_one(self.existing_user['username'])
        self.existing_user['hosts'].append(new_host)
        self.existing_user['uid_number'] = "4002"
        del self.existing_user['password']
        self.assertEquals(user, self.existing_user)

    def test_add_host_non_existant_username(self):
        with self.assertRaises(ValueError):
            babbage = "babbage.ug.eie.wits.ac.za"
            users.add_host('aslkjaslaksj', babbage)  # has no hosts

    def test_add_host_already_added(self):
        dummy = self.existing_user['hosts'][0]
        users.add_host(self.existing_user['username'], dummy)
        user = users.find_one(self.existing_user['username'])
        self.existing_user['uid_number'] = "4001"
        del self.existing_user['password']
        self.assertEquals(user, self.existing_user)

    def test_add_host_user_has_no_hosts(self):
        new_host = "testing.ug.eie.wits.ac.za"
        host_less = {"username": "hostless",
                     "first_name": "Host",
                     "last_name": "Less",
                     "email": ["host.less@students.wits.ac.za"],
                     "password": "nohost",
                     "yos": "1"}
        expected = {'username': 'hostless',
                    'gid_number': '1000',
                    'login_shell': '/bin/bash',
                    'first_name': 'Host',
                    'last_name': 'Less',
                    'hosts': ['testing.ug.eie.wits.ac.za'],
                    'home_directory': '/home/ug/hostless',
                    'uid_number': '1000',
                    'yos': '1',
                    'email': ['host.less@students.wits.ac.za']}
        users.delete(host_less['username'])
        users.add(host_less)
        users.add_host(host_less['username'], new_host)
        user = users.find_one(host_less['username'])
        self.assertEquals(user, expected)

    def test_remove_host(self):
        new_host = "testing.ug.eie.wits.ac.za"
        users.add_host(self.existing_user['username'], new_host)
        users.remove_host(self.existing_user['username'], new_host)
        user = users.find_one(self.existing_user['username'])
        self.existing_user['uid_number'] = "4001"
        del self.existing_user['password']
        self.assertEquals(user, self.existing_user)

    def test_remove_host_last_one(self):
        only_host = self.existing_user['hosts'][0]
        users.remove_host(self.existing_user['username'], only_host)
        user = users.find_one(self.existing_user['username'])
        self.existing_user['hosts'].remove(only_host)
        self.existing_user['uid_number'] = "4002"
        del self.existing_user['password']
        self.assertEquals(user, self.existing_user)

    def test_remove_host_not_there(self):
        fake_host = 'aslkajs'
        users.remove_host(self.existing_user['username'], fake_host)
        user = users.find_one(self.existing_user['username'])
        self.existing_user['uid_number'] = "4001"
        del self.existing_user['password']
        self.assertEquals(user, self.existing_user)

    def test_remove_host_non_existant_user(self):
        non_existant_user = 'aslkajs121'
        with self.assertRaises(ValueError):
            users.remove_host(non_existant_user, 'dummy')


if __name__ == "__main__":
    unittest.main()
