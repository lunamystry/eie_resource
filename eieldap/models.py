from eieldap import config
from eieldap.manager import Manager
from eieldap import logger


class User():

    def __init__(self, manager=None):
        if manager is None:
            manager = Manager(config)
        self.manager = manager
        self.basedn = "ou=people," + self.manager.base
        self.keymap = {"uid": "username",
                       "cn": "name",
                       "homeDirectory": "home_directory",
                       "loginShell": "login_shell",
                       "uidNumber": "uid_number",
                       "gidNumber": "gid_number",
                       "mail": "email"}
        self.inv_keymap = {v:k for k, v in self.keymap.items()}

    def save(self, attr):
        """ if the user exists update, if not create"""
        new_user = self.fix(attr, self.inv_keymap)
        user = self.manager.find_one(new_user)
        if user:
            logger.debug("updating user: " + str(new_user))
            self.manager.update(new_user)
            return True
        else:
            dn = "uid=" + new_user["uid"] + "," + self.basedn
            logger.debug("creating user(dn): " + str(dn))
            logger.debug("creating user(attr): " + str(new_user))
            self.manager.create(dn, new_user)
            return True
        return False

    def delete(self, uid):
        """ Deletes a user """
        dn = "uid=" + uid + "," + self.basedn
        #TODO: errors
        self.manager.delete(dn)

    def find(self):
        """ Returns all the people in the directory (think ldap)"""
        users = self.manager.find(self.basedn)
        users_list = []
        for user in users:
            new_user = self.fix(user, self.keymap)
            users_list.append(new_user)
        return users_list

    def find_one(self, attr):
        """ Returns a single user """
        user = self.manager.find_one(attr, self.basedn)
        return self.fix(user)

    def fix(self, user, keymap):
        new_user = {}
        for key in user.keys():
            try:
                nkey = keymap[key]
                new_user[nkey] = user[key]
            except KeyError:
                logger.debug("key not mapped: " + key)
        return new_user


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
    user = Users()
    print user.find()
    print user.find_one({"uid": "mandla"})
