from __future__ import print_function

import subprocess
import logging
import datetime

from eieldap import manager
from eieldap.descriptors import (String,
                                 SizedString,
                                 RegexString,
                                 IntSizedString,
                                 YearOfStudy,
                                 PasswordString)

logger = logging.getLogger(__name__)
basedn = "ou=people," + manager.base
default_password = "Dlab%s" % datetime.date.today().year


class User(object):
    '''
    This encapsulates converting and validating the user
     Password rules:
     1. No special characters allowed
     2. Space not allowed
     3. Min 6 Max 20
     4. At least one numeric character
     5. At least one capital letter
     6. Only two repetitive characters allowed

     Directory rules:
     1. Can contain dots
     2. Can contain "/"
     3. Can contain alphanumeric characters
     4. No spaces allowed
    '''
    first_name = SizedString()
    last_name = SizedString()
    yos = YearOfStudy(min=0, max=7)
    password = PasswordString(
        min=6,  # even though regex takes care of it
        max=20,
        pattern=r'^(?=.*[A-Z])(?=.*\d)(?!.*(.)\1\1)[a-zA-Z0-9@]{6,20}$'
        )
    username = SizedString(min=3)
    student_number = SizedString()  # thumb suck min length
    home_directory = RegexString(pattern=r'^[\/\_\.a-zA-Z0-9]*$')
    login_shell = RegexString(pattern=r'^[\/\_\.a-zA-Z0-9]*$')
    uid_number = IntSizedString(max=4)
    gid_number = IntSizedString(max=4)
    display_name = SizedString()
    samba_sid = SizedString()
    samba_nt_password = SizedString()
    samba_lm_password = SizedString()
    dn = String()
    emails = []
    hosts = []

    def __init__(self, username, yos, password, **kwargs):

        self.username = username
        self.yos = yos
        self.password = password

        # Default values
        self.display_name = username
        self.first_name = username
        self.last_name = username
        self.uid_number = str(self.next_uid_number(yos))
        self.gid_number = str(self.user_gid_number(yos))
        self.login_shell = '/bin/bash'
        self.home_directory = self.home_base(yos)

        # optional values take precedence except for samba_ntlm_passwords, dn,
        # samba_sid
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.dn = "uid=%s,%s" % (self.username, basedn)
        lm_password, nt_password = self.smb_encrypt(password)
        self.samba_nt_password = nt_password
        self.samba_lm_password = lm_password
        samba_rid = str(int(self.uid_number)*4)
        smbid_base = "S-1-5-21-3949128619-541665055-2325163404-"
        self.samba_sid = smbid_base + samba_rid

    def create(self):
        '''
        This will create the user with the given attributes on the ldap
        directory.

        example:
            User('Gunea', 'Pig', 1, 'password').create()
            monty = User('Monty', 'Python', 4, 'spam')
            monty.home_directory = '/home/england/pythonm'
            monty.create()
        '''
        try:
            manager.create(self.dn, self.as_ldap_attrs())
            self.set_password(self.password)
        except ValueError:
            error_msg = "user {} already exists".format(self.username)
            logger.error(error_msg)
            raise ValueError(error_msg)

    def update(self, attributes=None):
        '''
        This will try to update the User, throws an error if the username does
        not exist

        WARNING!!: If the even of an error called `Object class violation`, the
        user will be deleted and recreated with the attributes that were
        returned. I added this as a convinience for users added through Samba
        which may not have the correct ObjectClasses

        Password will not be updated by this function, it will not be passed
        out to the manager. If you want to change the password you have to use
        the set_password function.

        example:
            pigg = User.find('pigg')
            pigg.update({'first_name': 'Test', 'last_name': 'Subject'})
            pigg.home_directory = '/dev/null'
            pigg.update()
        '''
        if attributes:
            for key, attr in attributes.items():
                setattr(self, key, attr)
        ldap_attr = self.as_ldap_attrs()
        ldap_attr.pop('objectClass')
        try:
            manager.update(self.dn, ldap_attr)
        except ValueError as e:
            if str(e) == "Object class violation":
                manager.delete(self.dn)
                manager.create(self.dn, self.as_ldap_attrs())
            else:
                raise e

    def save(self):
        '''
        A convinince which will check if a user exists and then try to update
        the user. If the user does not exist, a new user is created.

        example:
            pigg = User('Gunea', 'Pig', 1, 'passing').save()
            new_attr = {'first_name': 'Passed'}
            testuser = User.find('testuser').save(new_attr)
            pigg.last_name = 'Pigs'
            pigg.save()
        '''
        existing = self.find(self.username)
        if existing:
            self.update()
        else:
            self.create()


    @classmethod
    def delete(cls, username):
        '''
        This will try to delete the user with the username given. If the user
        does not exist then nothing is done.

        example:
            User.delete('pigg')
        '''
        dn = "uid=%s,%s" % (username, basedn)
        manager.delete(dn)

    @classmethod
    def find(cls, username=None):
        '''
        If the username is given, it will try to find the user with the given
        username, if the username is not given, then if will return a list of
        all users.

        example:
            for user in User.find():
                print(user.display_name)
            pigg = User.find('pigg')
        '''
        if username:
            return User.find_one(username)

        users = manager.find(basedn, filter_key="uid")
        users_list = []
        for user in users:
            new_user = User.convert_from_ldap(user)
            users_list.append(new_user)
        return users_list

    @classmethod
    def find_one(cls, username):
        """ Returns a single user """
        attr = {}
        if username is not None:
            dn = "uid=" + username + "," + basedn
            attr = manager.find_by_dn(dn)

        if attr:
            attr = User.convert_from_ldap(attr)
        return attr

    @staticmethod
    def convert_from_ldap(user):
        '''Converts a user from LDAP format. If converting keys are not in the
        keymap passed, they will be removed from the result
        '''
        from_ldap_map = {"objectClass": "object_classes",
                         "uid": "username",
                         "cn": "first_name",
                         "sn": "last_name",
                         "homeDirectory": "home_directory",
                         "loginShell": "login_shell",
                         "uidNumber": "uid_number",
                         "gidNumber": "gid_number",
                         "sambaAcctFlags": "samba_acct_flags",
                         "sambaSID": "samba_sid",
                         "sambaNTPassword": "samba_nt_password",
                         "sambaLMPassword": "samba_lm_password",
                         "host": "hosts",
                         "mail": "emails"}

        new_user = {}
        if user:
            for key, val in user.items():
                try:
                    nkey = from_ldap_map[key]
                except KeyError:
                    continue  # if the key is not in the map i don't care
                if val == 'host' or val == 'mail':
                    new_user[nkey] = val
                else:
                    new_user[nkey] = str(val)

        if 'gidNumber' in user:
            new_user['yos'] = int(new_user['gid_number'])/1000
        else:
            new_user['yos'] = 0

        u = User(new_user['username'], new_user['yos'], 'dummyPa3sword')
        for key, attr in new_user.items():
            setattr(u, key, attr)

        return u

    def set_password(self, newpw):
        """ User the python ldap function to change the password
        of the user with the supplied username"""
        lm_password, nt_password = self.smb_encrypt(newpw)
        self.samba_nt_password = nt_password
        self.samba_lm_password = lm_password

        self.update()
        manager.set_password(self.dn, None, newpw)

    def smb_encrypt(self, password):
        ''' Calls an smbencrypt which comes with freeradius-utils on Ubuntu
        to encrypt the password given in smbencrypt form
        '''
        smbencrypt_output = subprocess.check_output(["smbencrypt", password])
        # carefully counted where the password starts in the returned string
        lm_password = smbencrypt_output[0:32].strip()
        nt_password = smbencrypt_output[32:].strip()
        return lm_password, nt_password

    def next_uid_number(self, yos):
        ''' Goes through all the uid numbers in the chosen year of study and
        returns an available one. In that year of study range. There are 1000
        available uid numbers in a range, if the number is reached, an
        exception is thrown yos can take on the following values

        0 - unknown
        1 - first year
        2 - second year
        3 - third year
        4 - fourth year
        5 - postgrad
        6 - staff
        7 - machine

        '''
        if yos not in range(0, 8):
            error_msg = "{} is out of uid/yos range".format(str(yos))
            logger.error(error_msg)
            raise ValueError(error_msg)
        all_users = manager.find(basedn, filter_key="uid")
        uids = []
        start_uid = yos*1000
        for user in all_users:
            try:
                uid = int(user['uidNumber'])
                if uid in range(start_uid, start_uid + 1000):
                    uids.append(uid)
            except KeyError:
                error_msg = "{} does not have a uid number".format(user['uid'])
                logger.warning(error_msg)
        for uid in range(start_uid, start_uid + 1000):
            if uid not in uids:
                return uid
        error_msg = "uid numbers for {} have been depleted".format(str(yos))
        logger.error(error_msg)
        raise RuntimeError(error_msg)  # How would anyone recover from this?

    def user_gid_number(self, yos):
        ''' There are 7 groups, depending on the year of study '''
        if yos not in range(0, 8):
            error_msg = "{} is out of uid/yos range".format(str(yos))
            logger.error(error_msg)
            raise ValueError(error_msg)

        return yos*1000

    def home_base(self, yos):
        ''' Home directory is changed based on the year of study
        '''
        if int(yos) < 5 and int(yos) > 0:
            home_base = "/home/ug/" + self.username
        elif int(yos) == 5:
            home_base = "/home/pg/" + self.username
        elif int(yos) == 6:
            home_base = "/home/staff/" + self.username
        elif int(yos) == 7 or int(yos) == 0:
            home_base = "/dev/null"
        else:
            error_msg = "Invalid Year of Study {}".format(yos)
            logger.error(error_msg)
            raise TypeError(error_msg)

        return home_base

    def add_host(self, host_domain):
        """ Allow the user with username to login to host with host_domain.
        this assumes the host has been configured to use the host property
        """
        if host_domain not in self.hosts:
            self.hosts.append(host_domain)
            self.update()

    def remove_host(username, host_domain):
        """ Disallow a user with username to login into a host with host_domain.
        this assumes the host has been configured to use the host property
        """
        if host_domain in self.hosts:
            self.hosts.remove(host_domain)
            self.update()

    def authenticate(self, password):
       return manager.authenticate(self.dn, password)

    def as_ldap_attrs(self):
        return {"objectClass": ["inetOrgPerson",
                                "organizationalPerson",
                                "posixAccount",
                                "sambaSamAccount",
                                "hostObject"],
                "uid": self.username,
                "cn": self.first_name,
                "sn": self.last_name,
                "homeDirectory": self.home_directory,
                "loginShell": self.login_shell,
                "uidNumber": self.uid_number,
                "gidNumber": self.gid_number,
                "sambaAcctFlags": "[U         ]",
                "sambaSID": self.samba_sid,
                "sambaNTPassword": self.samba_nt_password,
                "sambaLMPassword": self.samba_lm_password,
                "host": self.hosts,
                "mail": self.emails
                }

    def as_dict(self):
        return {"username": self.username,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "home_directory": self.home_directory,
                "login_shell": self.login_shell,
                "uid_number": self.uid_number,
                "gid_number": self.gid_number,
                "hosts": self.hosts,
                "emails": self.emails
                }

    def __str__(self):
        return str(self.as_dict())
