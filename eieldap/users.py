from __future__ import print_function

import subprocess
import logging

from eieldap import manager
from eieldap.descriptors import String
from eieldap.descriptors import SizedString
from eieldap.descriptors import RegexString
from eieldap.descriptors import IntSizedString
from eieldap.descriptors import YearOfStudy
from eieldap.descriptors import PasswordString

logger = logging.getLogger(__name__)
BASEDN = "ou=people," + manager.base


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
    first_name = SizedString(min=1)
    last_name = SizedString(min=1)
    yos = YearOfStudy(min=1, max=7)
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

    def __init__(self, first_name, last_name, yos, password, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.yos = yos
        self.password = password

        # Default values
        self.username = (last_name + first_name[0]).lower()
        self.uid_number = str(self.next_uid_number(yos))
        self.display_name = '%s %s' % (first_name, last_name)
        self.home_directory = '%s/%s' % (self.home_base(yos), self.username)
        self.gid_number = str(self.user_gid_number(yos))
        self.login_shell = '/bin/bash'

        # optional values take precedence except for samba_ntlm_passwords, dn,
        # samba_sid
        for key, val in kwargs.items():
            setattr(self, key, val)

        self.dn = "uid=%s,%s" % (self.username, BASEDN)
        lm_password, nt_password = self.smb_encrypt(password)
        self.samba_nt_password = nt_password
        self.samba_lm_password = lm_password
        samba_rid = str(int(self.uid_number)*4)
        smbid_base = "S-1-5-21-3949128619-541665055-2325163404-"
        self.samba_sid = smbid_base + samba_rid

    def smb_encrypt(self, password):
        """ Calls an smbencrypt which comes with freeradius-utils on Ubuntu
        to encrypt the password given in smbencrypt form
        """
        smbencrypt_output = subprocess.check_output(["smbencrypt", password])
        # carefully counted where the password starts in the returned string
        lm_password = smbencrypt_output[0:32].strip()
        nt_password = smbencrypt_output[32:].strip()
        return lm_password, nt_password

    def next_uid_number(self, yos):
        """ Goes through all the uid numbers in the chosen year of study and
        returns an available one. In that year of study range. There are 1000
        available uid numbers in a range, if the number is reached, an
        exception is thrown yos can take on the following values

        1 - first year
        2 - second year
        3 - third year
        4 - fourth year
        5 - postgrad
        6 - staff
        7 - machine

        """
        if yos not in range(1, 8):
            error_msg = "{} is out of uid/yos range".format(str(yos))
            logger.error(error_msg)
            raise ValueError(error_msg)
        all_users = manager.find(BASEDN, filter_key="uid")
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
        """ There are 7 groups, depending on the year of study """
        if yos not in range(1, 8):
            error_msg = "{} is out of uid/yos range".format(str(yos))
            logger.error(error_msg)
            raise ValueError(error_msg)

        return yos*1000

    def home_base(self, yos):
        """ Home directory is changed based on the year of study
        """
        if int(yos) < 5:
            home_base = "/home/ug"
        elif int(yos) == 5:
            home_base = "/home/pg"
        elif int(yos) == 6:
            home_base = "/home/staff"
        elif int(yos) == 7:
            home_base = "/dev/null"
        else:
            error_msg = "Invalid Year of Study {}".format(yos)
            logger.error(error_msg)
            raise TypeError(error_msg)

        return home_base

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
