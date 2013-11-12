from eieldap import config
from eieldap.manager import Manager
from eieldap import logger
import subprocess



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
