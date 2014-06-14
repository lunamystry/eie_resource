from eieldap.models import users
import unittest


class UserServicesTests(unittest.TestCase):

    def setUp(self):
        self.valid = {"username": "guneap",
                      "first_name": "Gunea",
                      "last_name": "Pig",
                      "email": "guneap@students.wits.ac.za",
                      "password": "passing",
                      "hosts": ['dummy'],
                      "yos": "1"}
        self.invalid = {"username": "testuser"}

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

    def test_validate_valid(self):
        users.validate(self.valid)

    def test_validate_invalid(self):
        with self.assertRaises(TypeError):
            users.validate(self.invalid)

    def test_convert_from_ldap(self):
        ldap_attr = {'dn': 'uid=monkeyl,ou=people,dc=eie,dc=wits,dc=ac,dc=za',
                     'displayName': 'Luffy Monkey',
                     'uid': 'monkeyl',
                     'objectClass': ['inetOrgPerson', 'organizationalPerson', 'posixAccount', 'sambaSamAccount', 'hostObject'],
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


class UsersTestCase(unittest.TestCase):

    def setUp(self):
        self.valid = {"username": "guneap",
                      "first_name": "Gunea",
                      "last_name": "Pig",
                      "email": "guneap@students.wits.ac.za",
                      "password": "passing",
                      "hosts": ['dummy'],
                      "yos": "1"}
        self.existing_user = {"username": "johnd",
                              "first_name": "John",
                              "last_name": "Doe",
                              "email": "mandla.niigata@students.wits.ac.za",
                              "password": "passing",
                              "hosts": ['dummy'],
                              "yos": "4"}
        self.missing_attributes = {"username": "johnd",
                                   "password": "passing",
                                   "hosts": ['dummy'],
                                   "yos": "4"}

    # def test_add(self):
    #     '''simply add a new valid user'''
    #     self.assertTrue(users.add(self.valid))

    # def test_add_existing(self):
    #     '''adding existing user should update it'''
    #     self.assertTrue(users.add(self.existing_user))

    # def test_add_missing_required_attributes(self):
    #     '''adding existing user should update it'''
    #     with self.assertRaises(TypeError):
    #         users.add(self.missing_attributes)

    # def test_save(self):
    #     """ Create a new user """
    #     pass
        # with self.assertRaises(TypeError):
        #     users.save(invalid_user)

        # Does not exist
        # if users.find_one(user_to_save['username']):
        #     users.delete(user=user_to_save)

        # # exists
        # user_to_save = {"username": "guneap",
        #                 "first_name": "Gunea",
        #                 "last_name": "Pig",
        #                 "email": "123@students.wits.ac.za",
        #                 "password": "passing",
        #                 "hosts": ['babbage.ug.eie.wits.ac.za', 'testing.ug.eie.wits.ac.za'],
        #                 "yos": "2"}
        # expected_user = {"username": "guneap",
        #                  "gid_number": "2000",
        #                  "login_shell": "/bin/bash",
        #                  "first_name": "Gunea",
        #                  "last_name": "Pig",
        #                  "yos": "2",
        #                  "hosts": ['babbage.ug.eie.wits.ac.za', 'testing.ug.eie.wits.ac.za'],
        #                  "home_directory": "/home/ug/guneap",
        #                  "uid_number": "2000",
        #                  "email": ["123@students.wits.ac.za"]}
        # if users.find_one(user_to_save['username']):
        #     users.delete(user=user_to_save)
        # self.assertTrue(users.save(user_to_save))
        # user = users.find_one("guneap")
        # self.assertEquals(user, expected_user)


    #     # raises an error if the number of valid uids has been reached

    # def test_add_host(self):
    #     """ Can I add a host?"""
    #     original_group = {"name": "natsuki", "members": ['mandla']}

    #     guneap = {"username": "guneap",
    #               "first_name": "Gunea",
    #               "last_name": "Pig",
    #               "email": ["123@students.wits.ac.za"],
    #               "password": "passing",
    #               "hosts": ['babbage.ug.eie.wits.ac.za'],
    #               "yos": "2"}
    #     expected_guneap = {"username": "guneap",
    #                        "gid_number": "2000",
    #                        "login_shell": "/bin/bash",
    #                        "first_name": "Gunea",
    #                        "last_name": "Pig",
    #                        "yos": "2",
    #                        "hosts": ['babbage.ug.eie.wits.ac.za', 'testing.ug.eie.wits.ac.za'],
    #                        "home_directory": "/home/ug/guneap",
    #                        "uid_number": "2000",
    #                        "email": ["123@students.wits.ac.za"]}
    #     johnd = {"username": "johnd",
    #               "first_name": "John",
    #               "last_name": "Doe",
    #               "email": ["john.doe@students.wits.ac.za"],
    #               "password": "passing",
    #               "yos": "4"}
    #     expected_johnd = {"username": "johnd",
    #                        "gid_number": "4000",
    #                        "login_shell": "/bin/bash",
    #                        "first_name": "John",
    #                        "last_name": "Doe",
    #                        "yos": "4",
    #                        "hosts": ['babbage.ug.eie.wits.ac.za'],
    #                        "home_directory": "/home/ug/johnd",
    #                        "uid_number": "4000",
    #                        "email": ["john.doe@students.wits.ac.za"]}
    #     already_member = johnd['username']
    #     existing_user = guneap['username']
    #     new_member = guneap['username']
    #     non_existing_user = "poiqaalkj"
    #     babbage = "babbage.ug.eie.wits.ac.za"
    #     testing = "testing.ug.eie.wits.ac.za"

    #     # remove from a group that exists
    #     user = users.find_one("guneap")
    #     if user:
    #         users.delete("guneap")
    #     self.assertTrue(users.save(guneap)) # save with one host
    #     user = users.find_one("mandla")
    #     if user:
    #         users.delete("johnd")
    #     self.assertTrue(users.save(johnd)) # no groups

    #     users.add_host(guneap['username'], babbage) # already there
    #     users.add_host(guneap['username'], testing)# new host for guneap
    #     g = users.find_one(guneap['username'])
    #     self.assertEquals(g, expected_guneap)
    #     users.add_host(johnd['username'], babbage) # has no hosts
    #     j = users.find_one(johnd['username'])
    #     self.assertEquals(j, expected_johnd)

    #     # what if user does not exist
    #     with self.assertRaises(ValueError):
    #         users.add_host(non_existing_user, babbage) # has no hosts

    # def test_remove_host(self):
    #     guneap = {"username": "guneap",
    #               "first_name": "Gunea",
    #               "last_name": "Pig",
    #               "email": ["123@students.wits.ac.za"],
    #               "password": "passing",
    #               "hosts": ['babbage.ug.eie.wits.ac.za', 'testing.ug.eie.wits.ac.za'],
    #               "yos": "2"}
    #     expected_guneap = {"username": "guneap",
    #                        "gid_number": "2000",
    #                        "login_shell": "/bin/bash",
    #                        "first_name": "Gunea",
    #                        "last_name": "Pig",
    #                        "yos": "2",
    #                        "hosts": ['babbage.ug.eie.wits.ac.za'],
    #                        "home_directory": "/home/ug/guneap",
    #                        "uid_number": "2000",
    #                        "email": ["123@students.wits.ac.za"]}
    #     non_existing_user = "poiqaalkj"
    #     babbage = "babbage.ug.eie.wits.ac.za"
    #     testing = "testing.ug.eie.wits.ac.za"

    #     # prepare
    #     user = users.find_one("guneap")
    #     if user:
    #         users.delete("guneap")
    #     self.assertTrue(users.save(guneap)) # save with one host

    #     # remove a host
    #     users.remove_host(guneap['username'], testing)
    #     g = users.find_one(guneap['username'])
    #     self.assertEquals(g, expected_guneap)

    #     # remove a host thats not there
    #     users.remove_host(guneap['username'], testing)
    #     self.assertEquals(g, expected_guneap)

    #     # remove the last host
    #     users.remove_host(guneap['username'], babbage)
    #     g = users.find_one(guneap['username'])
    #     del(expected_guneap['hosts'])
    #     self.assertEquals(g, expected_guneap)

    #     # remove from a user that does not exists
    #     with self.assertRaises(ValueError):
    #         users.remove_host(non_existing_user, babbage) # has no hosts

    # def test_change_password(self):
    #     """ I can change password """
    #     guneap = users.find_one('guneap')
    #     if not guneap:
    #         guneap = {"username": "guneap",
    #                   "first_name": "Gunea",
    #                   "last_name": "Pig",
    #                   "email": ["123@students.wits.ac.za"],
    #                   "password": "passing",
    #                   "hosts": ['babbage.ug.eie.wits.ac.za', 'testing.ug.eie.wits.ac.za'],
    #                   "yos": "2"}
    #         users.save(guneap)
    #     self.assertTrue(users.change_password('guneap', None, 'passing'))

    # def test_find_with_missing_attributes(self):
    #     """ I should be able to find even if some attributes are not there in
    #     the directory"""
    #     pass

    # def test_fix_gives_valid_user(self):
    #     user = {"uidNumber": 123}
    #     user = users.fix(user, users.keymap)
    #     print(user)


if __name__ == "__main__":
    unittest.main()
