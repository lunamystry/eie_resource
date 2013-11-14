from eieldap import manager
from eieldap import config
from eieldap import logger
import subprocess
import ldap


basedn = "ou=people," + manager.base
keymap = {"uid": "username",
          "cn": "first_name",
          "sn": "last_name",
          "homeDirectory": "home_directory",
          "loginShell": "login_shell",
          "uidNumber": "uid_number",
          "gidNumber": "gid_number",
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
        users_list.append(new_user)
    return users_list


def find_one(name=None, attr=None):
    """ Returns a single user """
    user = None
    if name is not None:
        dn = "uid=" + name + "," + basedn
        user = manager.find_by_dn(dn)
    elif attr is not None:
        fixed_user = fix(attr, inv_keymap)
        user = manager.find_one(fixed_user, basedn, filter_key="uid")

    if user:
        return fix(user, keymap)


def save(attr):
    """ if the user exists update, if not create"""
    fixed_user = fix(attr, inv_keymap)
    dn = "uid=" + fixed_user["uid"] + "," + basedn
    existing_user = manager.find_one(fixed_user, filter_key="uid")

    if existing_user:
        manager.update(dn, fixed_user)
        logger.info("updating user: " + str(dn))
        return True
    else:
        fixed_user["objectClass"] = ["account", "posixAccount", "sambaSamAccount"]
        fixed_user["uidNumber"] =
        fixed_user["homeDirectory"] = "/home/ug/" + fixed_user["uid"]
        lm_password, nt_password = smb_encrypt(attr["password"])
        fixed_user["sambaSID"] = "S-1-5-21-3949128619-541665055-2325163404-" + str(smbRid)
        fixed_user["sambaAcctFlags"] = "[U         ]"
        fixed_user["sambaNTPassword"] = nt_password
        fixed_user["sambaLMPassword"] = lm_password
        if 'dn' in fixed_user:
            del fixed_user['dn']
        manager.create(dn, fixed_user)
        logger.info("Created user: " + str(dn))
        return True
    return False


def delete(username=None, attr=None):
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
        manager.delete(dn)


def smb_encrypt(password):
    """ Calls an smbencrypt which comes with freeradius-utils on Ubuntu
    to encrypt the password given in smbencrypt form
    """
    smbencrypt_output = subprocess.check_output(["smbencrypt", password])
    lm_password = smbencrypt_output[0:32].strip()
    nt_password = smbencrypt_output[32:].strip()
    return lm_password, nt_password


def fix(user, keymap):
    if user:
        new_user = {}
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
    else:
        return user


def change_password(uid, oldpw, newpw):
    """ User the python ldap function to change the password
    of the user with the supplied uid"""
    dn = "uid=" + uid + "," + basedn
    user = manager.find_by_dn(dn)
    if user:
        logger.info("updating user: " + str(user))
        lm_password, nt_password = smb_encrypt(newpw)
        user["sambaNTPassword"] = nt_password
        user["sambaLMPassword"] = lm_password
        if manager.update(dn, user):
            return manager.change_password(dn, oldpw, newpw)
    return False


def authenticate(uid, password):
    dn = "uid=" + uid + "," + basedn
    return manager.authenticate(dn, password)
