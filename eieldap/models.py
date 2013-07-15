from eieldap import config
from eieldap.manager import Manager
from eieldap import logger


class User():
    keys = {"uid": "username",
            "cn": "name",
            "homeDirectory": "home_directory",
            "loginShell": "login_shell",
            "uidNumber": "uid_number",
            "gidNumber": "gid_number",
            "mail": "email"}

    def __init__(self, manager=None):
        if manager is None:
            manager = Manager(config)
        self.manager = manager
        self.basedn = "ou=people," + self.manager.base

    def save(self, attr):
        """ if the user exists update, if not create"""
        user = eieldap.find_one(attr["dn"])
        if user:
            eieldap.update(attr)
            return attr["dn"]
        else:
            eieldap.create(attr)
            return attr["dn"]
        return "error"

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
            new_user = self.fix(user)
            users_list.append(new_user)
        return users_list

    def find_one(self, attr):
        """ Returns a single user """
        user = self.manager.find_one(attr, self.basedn)
        return self.fix(user)

    def fix(self, user):
        new_user = {}
        for key in user.keys():
            try:
                nkey = self.keys[key]
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
        machine = eieldap.find_one(attr["dn"])
        if machine:
            eieldap.update(attr)
            return attr["dn"]
        else:
            eieldap.create(attr)
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
