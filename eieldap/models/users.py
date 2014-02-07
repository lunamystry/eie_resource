from eieldap import manager
from eieldap import config
from eieldap import logger
import subprocess
import ldap

# get email template with a lot of very useful information on it
# lecturer - 6000 -> 6099
# admin - 6100 -> 6199
# technical - 6200 -> 6299
# separate home directories for staff

basedn = "ou=people," + manager.base
keymap = {"uid": "username",
          "cn": "first_name",
          "sn": "last_name",
          "yos": "yos",
          "homeDirectory": "home_directory",
          "loginShell": "login_shell",
          "uidNumber": "uid_number",
          "gidNumber": "gid_number",
          "host": "hosts",
          "mail": "email"}
inv_keymap = {}
for k,v in keymap.items():
    inv_keymap[v] = k


def find():
    """ Returns all the people in the directory (think ldap)"""
    users = manager.find(basedn, filter_key="uid")
    users_list = []
    for user in users:
        new_user = fix(user, keymap)
        new_user['yos'] = int(new_user['gid_number'])/1000
        if new_user['email']:
            email = new_user['email'][0]
            new_user['student_number'] = email[:email.find('@')]
        users_list.append(new_user)
    return users_list


def find_one(username=None, attr=None):
    """ Returns a single user """
    user = None
    if username is not None:
        dn = "uid=" + username + "," + basedn
        user = manager.find_by_dn(dn)
    elif attr is not None:
        fixed_user = fix(attr, inv_keymap)
        user = manager.find_one(fixed_user, basedn, filter_key="uid")

    if user:
        user['yos'] = str(int(user['gidNumber'])/1000)
        return fix(user, keymap)


def add(attr):
    """ adds a new user """
    required_attributes = ['first_name', 'last_name', 'yos', 'email', 'password']
    for attribute in required_attributes:
        if attribute not in attr:
            raise TypeError("You have a missing attributes: " + attribute)
    fixed_user = fix(attr, inv_keymap)
    dn = "uid=" + fixed_user["uid"] + "," + basedn

    uid_number = next_uid_number(int(attr['yos']))
    gid_number = user_gid_number(int(attr['yos']))
    lm_password, nt_password = smb_encrypt(attr["password"])
    smbRid = uid_number*4
    if int(attr['yos']) < 5:
        home_base = "/home/ug"
    elif int(attr['yos']) == 5:
        home_base = "/home/pg"
    elif int(attr['yos']) == 6:
        home_base = "/home/staff"
    elif int(attr['yos']) == 7:
        home_base = "/dev/null"
    else:
        error_msg = "trying to save but Year of Study " + attr['yos'] + " is invalid"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    fixed_user["objectClass"] = ["inetOrgPerson", "organisationalPerson", "posixAccount", "sambaSamAccount", "hostObject"]
    fixed_user["uidNumber"] = str(uid_number)
    fixed_user["gidNumber"] = str(gid_number)
    fixed_user["homeDirectory"] = "/home/ug/" + fixed_user["uid"]
    fixed_user["loginShell"] = "/bin/bash"
    fixed_user["displayName"] = fixed_user["cn"] + " " + fixed_user["sn"]
    fixed_user["sambaSID"] = "S-1-5-21-3949128619-541665055-2325163404-" + str(smbRid)
    fixed_user["sambaAcctFlags"] = "[U         ]"
    fixed_user["sambaNTPassword"] = nt_password
    fixed_user["sambaLMPassword"] = lm_password
    if 'dn' in fixed_user:
        del fixed_user['dn']
    if 'yos' in fixed_user:
        del fixed_user['yos']
    try:
        for index, host in enumerate(fixed_user["host"]):
            fixed_user["host"][index] = str(host)
    except KeyError:
        pass
    if manager.create(dn, fixed_user):
        change_password(fixed_user['uid'], None, attr['password'])
        logger.info("Created user: " + str(dn))
        return True
    logger.info("user could not be created: " + str(fixed_user))
    return False


def update(attr):
    """ updates a new user"""
    fixed_user = fix(attr, inv_keymap)
    dn = "uid=" + fixed_user["uid"] + "," + basedn
    existing_user = manager.find_one(fixed_user, filter_key="uid")

    gid_number = user_gid_number(int(attr['yos']))
    if 'yos' in fixed_user:
        del fixed_user['yos']
    fixed_user["gidNumber"] = str(gid_number)
    try:
        for index, host in enumerate(fixed_user["host"]):
            fixed_user["host"][index] = str(host)
    except KeyError:
        pass
    if manager.update(dn, fixed_user):
        logger.info("updated user: " + str(dn))
        return True
    return False

def save(attr):
    """ if the user exists update, if not create"""
    if 'username' not in attr:
        raise TypeError("You have a missing attributes: username")

    fixed_user = fix(attr, inv_keymap)
    dn = "uid=" + fixed_user["uid"] + "," + basedn
    existing_user = manager.find_one(fixed_user, filter_key="uid")

    if existing_user:
        return update(attr)
    else:
        return add(attr)
    return False


def delete(username=None, user=None):
    """ Deletes a user """
    existing_user = None
    if username is not None:
        dn = "uid=" + username + "," + basedn
        existing_user = manager.find_by_dn(dn)
    elif user is not None:
        fixed_user = fix(user, inv_keymap)
        dn = "uid=" + fixed_user['uid'] + "," + basedn
        existing_user = manager.find_one(fixed_user, basedn, filter_key="uid")

    if existing_user:
        if manager.delete(existing_user['dn']):
            logger.info("deleted: " + existing_user['dn'])
            return True
    return False


def smb_encrypt(password):
    """ Calls an smbencrypt which comes with freeradius-utils on Ubuntu
    to encrypt the password given in smbencrypt form
    """
    smbencrypt_output = subprocess.check_output(["smbencrypt", password])
    lm_password = smbencrypt_output[0:32].strip()
    nt_password = smbencrypt_output[32:].strip()
    return lm_password, nt_password


def fix(user, keymap):
    new_user = {}
    for key in keymap:
        if keymap[key] == 'uid_number' or keymap[key] == 'gid_number':
            new_user[keymap[key]] = 0
        elif keymap[key] == 'hosts' or keymap[key] == 'email' or keymap[key] == 'host':
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
                logger.debug("key not mapped: " + key)
    return new_user


def change_password(uid, oldpw, newpw):
    """ User the python ldap function to change the password
    of the user with the supplied uid"""
    dn = "uid=" + uid + "," + basedn
    user = manager.find_by_dn(dn)
    if user:
        lm_password, nt_password = smb_encrypt(newpw)
        user["sambaNTPassword"] = nt_password
        user["sambaLMPassword"] = lm_password
        logger.debug("Updating password for user: " + str(user['dn']))
        dn = user['dn']
        if manager.update(dn, user):
            return manager.change_password(dn, oldpw, newpw)
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
            save(user)
    except KeyError:
        user['hosts'] = [host_domain]
        save(user)


def remove_host(username, host_domain):
    """ Disallow a user with username to login into a host with host_domain.
    this assumes the host has been configured to use the host property"""
    user = find_one(username)
    if not user:
        raise ValueError("trying to add host {1} to {0}, but {0} does not exist in the ldap".format(username, host_domain))

    if host_domain in user['hosts']:
        user['hosts'].remove(host_domain)
        save(user)
    else:
        logger.debug("host: {0} not found in {1} user".format(host_domain, username))


def authenticate(username, password):
    dn = "uid=" + username + "," + basedn
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
        logger.error("Tried to add out of range uid/yos")
        raise ValueError("The Year of Study: " + str(yos) + " is out of range")
    all_users = find()
    uids = []
    start_uid = yos*1000
    for user in all_users:
        try:
            uid = int(user['uid_number'])
            if uid in range(start_uid, start_uid + 1000):
                uids.append(uid)
        except KeyError:
            logger.error(user['username'] + " does not have a uid number")
    for uid in range(start_uid, start_uid + 1000):
        if uid not in uids:
            return uid
    error_msg = "All uid numbers have for " + str(yos) + " Year of Study have been depleted"
    logger.error(error_msg)
    raise RuntimeError(error_msg)


def user_gid_number(yos):
    """ There are 7 groups, depending on the year of study """
    if yos not in range(1, 8):
        logger.error("Tried to add out of range uid/yos")
        raise ValueError("The Year of Study: " + str(yos) + " is out of range")

    return yos*1000
