from eieldap import manager
import subprocess
import logging
import time

# get email template with a lot of very useful information on it
# lecturer - 6000 -> 6099
# admin - 6100 -> 6199
# technical - 6200 -> 6299
# separate home directories for staff

logger = logging.getLogger("eieldap.models.users")
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


class User():
    """This encapsulates converting and validating the user"""
    dn = None
    attributes = {"objectClass": ["inetOrgPerson", "organizationalPerson",
                  "posixAccount", "sambaSamAccount", "hostObject"],
                  "uidNumber": None,
                  "gidNumber": None,
                  "homeDirectory": None,
                  "loginShell": "/bin/bash",
                  "displayName": None,
                  "sambaSID": None,
                  "sambaAcctFlags": "[U         ]",
                  "sambaNTPassword": None,
                  "sambaLMPassword": None}

    def __init__(self, attr):
        validate(attr)
        self.set_attributes(attr)

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
        self.attributes['cn'] = attr['first_name']
        self.attributes['sn'] = attr['last_name']
        self.attributes['uidNumber'] = str(next_uid_number(int(attr['yos'])))
        self.attributes['gidNumber'] = str(user_gid_number(int(attr['yos'])))
        lm_password, nt_password = smb_encrypt(attr["password"])
        self.attributes['sambaNTPassword'] = nt_password
        self.attributes['sambaLMPassword'] = lm_password
        smbRid = self.attributes['uidNumber']*4
        self.attributes["sambaSID"] = "S-1-5-21-3949128619-541665055-2325163404-{}".format(str(smbRid))
        self.attributes["homeDirectory"] = "{0}/{1}".format(home_base,
                                                            attr["username"])
        self.attributes["loginShell"] = "/bin/bash"
        self.attributes["displayName"] = "{0} {1}".format(attr["first_name"],
                                                          attr["last_name"])
        try:
            self.attributes["host"] = attr['hosts']
            self.attributes["mail"] = [attr['email']]
        except KeyError:
            pass


def add(attr):
    """ adds a new user """
    user = User(attr)
    if manager.create(user.dn, user.attributes):
        change_password(user.attributes['uid'], None, attr['password'])
        logger.info("created user: {}".format(user.dn))
        return True
    return False


def find():
    """ Returns all the people in the directory (think ldap)"""
    users = manager.find(BASEDN, filter_key="uid")
    users_list = []
    for user in users:
        new_user = convert(user, FROM_LDAP_MAP)
        new_user['yos'] = int(new_user['gid_number'])/1000
        if new_user['email']:
            email = new_user['email'][0]
            new_user['student_number'] = email[:email.find('@')]
        users_list.append(new_user)
    return users_list


# def find_one(username=None, attr=None):
#     """ Returns a single user """
#     user = None
#     if username is not None:
#         dn = "uid=" + username + "," + BASEDN
#         user = manager.find_by_dn(dn)
#     elif attr is not None:
#         fixed_user = fix(attr, inv_keymap)
#         user = manager.find_one(fixed_user, BASEDN, filter_key="uid")
#
#     if user:
#         user['yos'] = str(int(user['gidNumber'])/1000)
#         return fix(user, keymap)
#
#
# def update(attr):
#     """ updates a user"""
#     fixed_user = fix(attr, inv_keymap)
#     dn = "uid=" + fixed_user["uid"] + "," + BASEDN
#     existing_user = manager.find_one(fixed_user, filter_key="uid")
#
#     gid_number = user_gid_number(int(attr['yos']))
#     if 'yos' in fixed_user:
#         del fixed_user['yos']
#     fixed_user["gidNumber"] = str(gid_number)
#     try:
#         for index, host in enumerate(fixed_user["host"]):
#             fixed_user["host"][index] = str(host)
#     except KeyError:
#         pass
#
#     if manager.update(dn, fixed_user):
#         logger.info("updated user: " + str(dn))
#         return True
#     return False
#
#
# def save(attr):
#     """ if the user exists update, if not create"""
#     if 'username' not in attr:
#         raise TypeError("You have a missing attributes: username")
#
#     fixed_user = fix(attr, inv_keymap)
#     dn = "uid=" + fixed_user["uid"] + "," + BASEDN
#     existing_user = manager.find_one(fixed_user, filter_key="uid")
#
#     if existing_user:
#         return update(attr)
#     else:
#         return add(attr)
#     return False
#
#
# def delete(username=None, user=None):
#     """ Deletes a user """
#     existing_user = None
#     if username is not None:
#         dn = "uid=" + username + "," + BASEDN
#         existing_user = manager.find_by_dn(dn)
#     elif user is not None:
#         fixed_user = fix(user, inv_keymap)
#         dn = "uid=" + fixed_user['uid'] + "," + BASEDN
#         existing_user = manager.find_one(fixed_user, BASEDN, filter_key="uid")
#
#     if existing_user:
#         if manager.delete(existing_user['dn']):
#             logger.info("deleted: " + existing_user['dn'])
#             return True
#     return False

def validate(attr):
    '''Make sure that attributes are all there in the correct form'''
    required_attributes = ['first_name', 'last_name', 'yos', 'email',
                           'password']
    for attribute in required_attributes:
        if attribute not in attr:
            raise TypeError("missing attributes: {}".format(
                attribute))


def convert(user, keymap):
    '''DESTRUCTIVE: Converts a user either from LDAP form or to depending on 
    keymap. If converting keys are not in the keymap passed, they will be
    removed from the result'''
    if user is None:
        return None
    new_user = {}
    for key in keymap:
        if keymap[key] == 'uid_number' or keymap[key] == 'gid_number':
            new_user[keymap[key]] = 0
        elif (keymap[key] == 'hosts'
                or keymap[key] == 'email'
                or keymap[key] == 'host'):
            new_user[keymap[key]] = []
        else:
            new_user[keymap[key]] = None

    if user:
        for key in user.keys():
            try:
                nkey = keymap[key]
                if type(user[key]) is list:
                    new_user[nkey] = user[key]
                else:
                    new_user[nkey] = str(user[key])
            except KeyError:
                pass
    return new_user


def smb_encrypt(password):
    """ Calls an smbencrypt which comes with freeradius-utils on Ubuntu
    to encrypt the password given in smbencrypt form
    """
    smbencrypt_output = subprocess.check_output(["smbencrypt", password])
    lm_password = smbencrypt_output[0:32].strip()
    nt_password = smbencrypt_output[32:].strip()
    return lm_password, nt_password


def change_password(username, oldpw, newpw):
    """ User the python ldap function to change the password
    of the user with the supplied username"""
    dn = "uid=" + username + "," + BASEDN
    user = manager.find_by_dn(dn)
    if user:
        lm_password, nt_password = smb_encrypt(newpw)
        user["sambaNTPassword"] = nt_password
        user["sambaLMPassword"] = lm_password
        dn = user['dn']
        if manager.update(dn, user):
            return manager.change_password(dn, oldpw, newpw)
    return False


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
            return manager.change_password(dn, None, newpw)
    return False


# def add_host(username, host_domain):
#     """ Allow the user with username to login to host with host_domain.
#     this assumes the host has been configured to use the host property"""
#     user = find_one(username)
#     if not user:
#         raise ValueError("trying to add host {1} to {0}, but {0} does not exist in the ldap".format(username, host_domain))
#
#     try:
#         if host_domain not in user['hosts']:
#             user['hosts'].append(host_domain)
#             save(user)
#     except KeyError:
#         user['hosts'] = [host_domain]
#         save(user)
#
#
# def remove_host(username, host_domain):
#     """ Disallow a user with username to login into a host with host_domain.
#     this assumes the host has been configured to use the host property"""
#     user = find_one(username)
#     if not user:
#         raise ValueError("trying to add host {1} to {0}, but {0} does not exist in the ldap".format(username, host_domain))
#
#     if host_domain in user['hosts']:
#         user['hosts'].remove(host_domain)
#         save(user)
#     else:
#         logger.debug("host: {0} not found in {1} user".format(
#             host_domain, username))


def authenticate(username, password):
    dn = "uid=" + username + "," + BASEDN
    return manager.authenticate(dn, password)


def next_uid_number(yos):
    """ Goes through all the uid numbers in the chosen year of study and returns
    an available one. In that year of study range. There are 1000 available
    uid numbers in a range, if the number is reached, an exception is thrown
    yos can take on the following values

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
            logger.error(error_msg)
            raise TypeError(error_msg)
    for uid in range(start_uid, start_uid + 1000):
        if uid not in uids:
            return uid
    error_msg = "uid numbers have for {} have been depleted".format(str(yos))
    logger.error(error_msg)
    raise RuntimeError(error_msg)


def user_gid_number(yos):
    """ There are 7 groups, depending on the year of study """
    if yos not in range(1, 8):
        error_msg = "{} is out of uid/yos range".format(str(yos))
        logger.error(error_msg)
        raise ValueError(error_msg)

    return yos*1000
