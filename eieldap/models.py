from eieldap import config
from eieldap.manager import Manager


class Users():
    first_name = None
    last_name = None
    username = None
    yos = None
    nt_password = None
    lm_password = None
    plain_password = None
    uid_number = None
    gid_number = None
    smb_rid = None

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
        return self.manager.find(self.basedn)

    def find_one(self, attr):
        """ Returns a single user """
        return self.manager.find_one(attr, self.basedn)


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
