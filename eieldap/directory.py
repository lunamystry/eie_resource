# commandline:
#  ldapsearch -xLLL -H <host> -b <base> <search>
from ConfigParser import SafeConfigParser
import ldap


class EIELdap():
    """This a module to help with managing the eieldap using python"""

    def __init__(self,  config_location):
        self.connect(config_location)

    def __del__(self):
        self.disconnect()

    def connect(self, config_location):
        cfg = SafeConfigParser()
        cfg.read(config_location)
        self.server = cfg.get("ldap", "server")
        self.dn = cfg.get("ldap", "dn")
        self.pw = cfg.get("ldap", "pw")
        self.base = cfg.get("ldap", "base")
        self.connection = ldap.initialize('ldap://'+self.server)
        self.connection.simple_bind_s(self.dn, self.pw)

    def disconnect(self):
        self.connection.unbind()

    def create(self, dn, attr):
        modlist = []
        for key in attr.keys():
            modlist.append((key, attr[key]))
        # TODO: Error checking
        self.connection.add_s(dn, modlist)

    def update(self, dn, attr):
        """ Attr is a dictionary of values for a single thing"""
        modlist = []
        for key in attr.keys():
            modlist.append((ldap.MOD_REPLACE, key, attr[key]))
        # TODO: Error checking
        self.connection.modify_s(dn, modlist)

    def delete(self, dn):
        self.connection.delete_s(dn)

    def print_exception(self, exception):
        args = exception.args[0]  # Accessing using 0 feels wrong
        print "ERROR: Could not change password "
        print "INFO:", args["info"]
        print "DESC:", args["desc"]

    def change_password(self, username, oldpw, newpw):
        """ User the python ldap function to change the passord
        of the user with the supplied uid"""
        dn = username + self.base
        print dn
        try:
            self.connection.passwd_s(dn, None, newpw)
        except Exception as e:
            print e

    def authenticate(self, username, password):
        dn = username + self.base
        # first search for the username. Each username is unique for
        # each user.
        self.connection.bind_s(dn, password)
        return True

    def find(self):
        result = manager.connection.search_s(
            manager.base, ldap.SCOPE_SUBTREE, attr["uid"])
        if result[]:
            return result

    def find_one(self, attr):
        result = manager.connection.search_s(
            manager.base, ldap.SCOPE_SUBTREE, attr["uid"])
        if result:
            return result[0]
        else:
            return "Error, nothing found"


if __name__ == '__main__':
    manager = EIELdap('../config/ldap.cfg')
    r = manager.connection.search_s(manager.base, ldap.SCOPE_SUBTREE, 'uid=*')
    # for dn, entry in r:
    #     print dn
    #     print 'Processing: ', repr(entry['uid'][-1])
    #     print entry
    r = manager.connection.search_s(manager.base, ldap.SCOPE_SUBTREE, 'uid=mandla')
    print r
    # dn = "cn=Leonard Mbuli,ou=people," + manager.base
    # manager.update(dn, {"description": "Extraordinary fellow"})
    # username = "lunamystry"
    # first_name = "Mandla"
    # last_name = "Mbuli"
    # uid_number = 7000
    # gid_number = 8000
    # smb_rid = 231
    # dn = "cn=Mandla Mbuli,ou=people," + manager.base
    # user = {
    #      # "dn": "uid=" + username + ",ou=ug,dc=eie,dc=wits,dc=ac,dc=za",
    #      "objectclass": ["account", "posixAccount"],
    #      "cn": first_name + " " + last_name,
    #      "uid": username,
    #      # "displayName": first_name + " " + last_name,
    #      "uidNumber": str(uid_number),
    #      "gidNumber": str(gid_number),
    #      "homeDirectory": "/home/ug/" + username,
    #      "loginShell": "/bin/bash",
    #      # "sambaSID": "S-1-5-21-3949128619-541665055-2325163404-" + str(smb_rid),
    #      # "sambaAcctFlags": "[U         ]",
    #      # "sambaNTPassword": nt_password,
    #      # "sambaLMPassword": lm_password
    # }
    # manager.create(dn, user)
    # manager.delete(dn)
    # print manager.authenticate('cn=Leonard Mbuli,ou=people,', "passing")
    # print manager.change_password('cn=Leonard Mbuli,ou=people,',
    #                               "pass",
    #                               "passing")
    # manager.change_password('uid=leny,ou=ug,'+manager.base,'pass', 'passing')
