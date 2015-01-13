from __future__ import print_function

import subprocess
import logging
import time

from eieldap import manager

# get email template with a lot of very useful information on it
# lecturer - 6000 -> 6099
# admin - 6100 -> 6199
# technical - 6200 -> 6299
# separate home directories for staff

logger = logging.getLogger(__name__)
BASEDN = "ou=people," + manager.base
FROM_LDAP_MAP = {"uid": "username",
                 "cn": "first_name",
                 "sn": "last_name",
                 "homeDirectory": "home_directory",
                 "loginShell": "login_shell",
                 "uidNumber": "uid_number",
                 "gidNumber": "gid_number",
                 "host": "hosts",
                 "mail": "email"}
TO_LDAP_MAP = {}
for k, v in FROM_LDAP_MAP.items():
    TO_LDAP_MAP[v] = k


# class List(Typed):
#     ty = list
#
#     def __set__(self, instance, value):
#         if not isinstance(value, list):
#             raise TypeError('Expected %s' % self.ty)  # don't need Typed
#         bstringed = [str(item) for item in value]  # convert to bytestring
#         super(List, self).__set__(instance, bstringed)


    # emails = List()
    # hosts = List()


    def set_attributes(self, attr):
        '''Set the attributes'''
        self.dn = "uid=" + attr["username"] + "," + BASEDN
        if int(attr['yos']) < 5:
            home_base = "/home/ug"
        elif int(attr['yos']) == 5:
            home_base = "/home/pg"
        elif int(attr['yos']) == 6:
            home_base = "/home/staff"
        elif int(attr['yos']) == 7:
            home_base = "/dev/null"
        else:
            error_msg = "Invalid Year of Study {}".format(attr['yos'])
            logger.error(error_msg)
            raise TypeError(error_msg)
        self.attributes['cn'] = str(attr['first_name'])
        self.attributes['sn'] = str(attr['last_name'])
        self.attributes['uidNumber'] = str(next_uid_number(int(attr['yos'])))
        self.attributes['gidNumber'] = str(user_gid_number(int(attr['yos'])))
        smbRid = str(int(self.attributes['uidNumber'])*4)
        self.attributes["sambaSID"] = "S-1-5-21-3949128619-541665055-2325163404-{}".format(str(smbRid))
        self.attributes["displayName"] = "{0} {1}".format(attr["first_name"],
                                                          attr["last_name"])
        if 'password' in attr:
            lm_password, nt_password = smb_encrypt(attr["password"])
            self.attributes['sambaNTPassword'] = nt_password
            self.attributes['sambaLMPassword'] = lm_password
        if 'email' in attr:
            if not isinstance(attr['email'], list):
                raise TypeError("email must be in a list")
            else:
                self.attributes["mail"] = [str(email) for email in
                                           attr['email']]
        if "hosts" in attr:
            if not isinstance(attr['hosts'], list):
                raise TypeError("hosts must be in a list")
            self.attributes["host"] = [str(host) for host in attr['hosts']]
        if 'login_shell' in attr:
            self.attributes["loginShell"] = str(attr['login_shell'])
        if 'username' in attr:
            self.attributes['uid'] = str(attr['username'])
        else:
            # TODO: What if username already exists?
            self.attributes['uid'] = str(attr['last_name'] + attr['first_name'][0])
        if 'home_directory' in attr:
            self.attributes['homeDirectory'] = str(attr['home_directory'])
        else:
            self.attributes["homeDirectory"] = "{0}/{1}".format(
                home_base,
                self.attributes["uid"])


def add(attr):
    """ adds a new user """
    user = User(attr)
    try:
        manager.create(user.dn, user.attributes)
        if 'password' in attr:
            set_password(user.attributes['uid'], None, attr['password'])
    except ValueError:
        error_msg = "user {} already exists".format(attr['username'])
        logger.error(error_msg):
        raise ValueError(error_msg)


def update(attr):
    """ updates a user"""
    user = User(attr)
    manager.update(user.dn, user.attributes)
    if 'password' in attr:
        set_password(user.attributes['uid'], None, attr['password'])


def delete(username=None, user=None):
    """ Deletes a user """
    existing_user = None
    if username is None or not isinstance(username, str):
        if user is not None:
            username = user['username']
        else:
            return

    dn = "uid=" + username + "," + BASEDN
    existing_user = manager.find_by_dn(dn)

    if existing_user:
        if manager.delete(existing_user['dn']):
            logger.info("deleted: " + existing_user['dn'])


def validate(attr):
    '''Make sure that attributes are all there in the correct form'''
    required_attributes = ['first_name', 'last_name', 'yos', 'email']
    for attribute in required_attributes:
        if attribute not in attr:
            raise TypeError("missing attributes: {}".format(
                attribute))




def reset_password(username):
    """ User the python ldap function to reset the password
    of the user with the supplied username"""
    newpw = "dlab"+str(time.strftime("%Y"))
    dn = "uid=" + username + "," + BASEDN
    user = manager.find_by_dn(dn)
    if user:
        lm_password, nt_password = smb_encrypt(newpw)
        user["sambaNTPassword"] = nt_password
        user["sambaLMPassword"] = lm_password
        logger.debug("Changing password for user with dn: " + str(user['dn']))
        dn = user['dn']
        if manager.update(dn, user):
            return manager.set_password(dn, None, newpw)
    return False


def add_host(username, host_domain):
    """ Allow the user with username to login to host with host_domain.
    this assumes the host has been configured to use the host property"""
    user = find_one(username)
    if not user:
        raise ValueError("trying to add host {1} to {0}, but {0} does not exist in the ldap".format(username, host_domain))

    try:
        if host_domain not in user['hosts']:
            user['hosts'].append(host_domain)
            update(user)
    except KeyError:
        user['hosts'] = [host_domain]
        update(user)


def remove_host(username, host_domain):
    """ Disallow a user with username to login into a host with host_domain.
    this assumes the host has been configured to use the host property"""
    user = find_one(username)
    if not user:
        raise ValueError("trying to add host {1} to {0}, but {0} does not exist in the ldap".format(username, host_domain))

    if host_domain in user['hosts']:
        user['hosts'].remove(host_domain)
        update(user)
    else:
        logger.debug("host: {0} not found in {1} user".format(
            host_domain, username))


def authenticate(username, password):
    dn = "uid=" + username + "," + BASEDN
    return manager.authenticate(dn, password)
