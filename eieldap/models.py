from eieldap import config
from eieldap.manager import Manager
from eieldap import logger
import subprocess


class User():

    def __init__(self, manager=None):
        if manager is None:
            manager = Manager(config)
        self.manager = manager
        self.basedn = "ou=people," + self.manager.base
        self.keymap = {"dn": "id",
                       "uid": "username",
                       "cn": "name",
                       "homeDirectory": "home_directory",
                       "loginShell": "login_shell",
                       "uidNumber": "uid_number",
                       "gidNumber": "gid_number",
                       "mail": "email"}
        self.inv_keymap = {}
        for k,v in self.keymap.items():
            self.inv_keymap[v] = k

    def save(self, attr):
        """ if the user exists update, if not create"""
        new_user = self.fix(attr, self.inv_keymap)
        user = self.manager.find_one(new_user)
        if user:
            logger.info("updating user: " + str(new_user))
            self.manager.update(new_user)
            return True
        else:
            dn = "uid=" + new_user["uid"] + "," + self.basedn
            logger.info("creating user(dn): " + str(dn))
            logger.debug("creating user(attr): " + str(new_user))
            # new_user["objectClass"] = ["account", "posixAccount", "sambaSamAccount"]
            # new_user["uidNumber"] =
            # new_user["uidNumber"] =
            # new_user["homeDirectory"] = "/home/ug/" + uid
            # lm_password, nt_password = smb_encrypt(attr["password"])
            # new_user["sambaSID"] = "S-1-5-21-3949128619-541665055-2325163404-" + str(smbRid)
            # new_user["sambaAcctFlags"] = "[U         ]"
            # new_user["sambaNTPassword"] = nt_password
            # new_user["sambaLMPassword"] = lm_password
            self.manager.create(dn, new_user)
            return True
        return False

    def smb_encrypt(self, password):
        """ Calls an smbencrypt which comes with freeradius-utils on Ubuntu
        to encrypt the password given in smbencrypt form
        """
        smbencrypt_output = subprocess.check_output(["smbencrypt", password])
        lm_password = smbencrypt_output[0:32].strip()
        nt_password = smbencrypt_output[32:].strip()
        return lm_password, nt_password

    def delete(self, uid):
        """ Deletes a user """
        dn = "uid=" + uid + "," + self.basedn
        self.manager.delete(dn)

    def find(self):
        """ Returns all the people in the directory (think ldap)"""
        users = self.manager.find(self.basedn)
        users_list = []
        for user in users:
            new_user = self.fix(user, self.keymap)
            users_list.append(new_user)
        return users_list

    def change_password(self, uid, oldpw, newpw):
        """ User the python ldap function to change the password
        of the user with the supplied uid"""
        dn = "uid=" + uid + "," + self.basedn
        user = self.manager.find_by_dn(dn)
        if user:
            logger.info("updating user: " + str(user))
            lm_password, nt_password = self.smb_encrypt(newpw)
            user["sambaNTPassword"] = nt_password
            user["sambaLMPassword"] = lm_password
            if self.manager.update(dn, user):
                return self.manager.change_password(dn, oldpw, newpw)
        return False

    def authenticate(self, uid, password):
        dn = "uid=" + uid + "," + self.basedn
        return self.manager.authenticate(dn, password)

    def find_one(self, attr):
        """ Returns a single user """
        ldap_attr = self.fix(attr, self.inv_keymap)
        user = self.manager.find_one(ldap_attr, self.basedn)
        if user:
            return self.fix(user, self.keymap)

    def fix(self, user, keymap):
        if user:
            new_user = {}
            for key in user.keys():
                try:
                    nkey = keymap[key]
                    new_user[nkey] = user[key]
                except KeyError:
                    logger.debug("key not mapped: " + key)
            return new_user
        else:
            return user


class Machines():
    def __init__(self, manager=None):
        if manager is None:
            manager = Manager(config)
        self.manager = manager
        self.basedn = "ou=machines," + self.manager.base

    def save(self, attr):
        """ if the machine exists update, if not create"""
        machine = manager.find_one(attr["dn"])
        if machine:
            manager.update(attr)
            return attr["dn"]
        else:
            manager.create(attr)
            return attr["dn"]
        return "error"

    def delete(self, uid):
        """ Deletes a machine """
        dn = "uid=" + uid + "," + self.basedn
        #TODO: errors
        self.manager.delete(dn)

    def find(self):
        """ Returns all the people in the directory (think ldap)"""
        return self.manager.find(self.basedn)

    def find_one(self, attr):
        """ Returns a single machine """
        return self.manager.find_one(attr, self.basedn)


if __name__ == "__main__":
    user = User()
    print user.find()
    print user.find_one({"uid": "mandla"})
