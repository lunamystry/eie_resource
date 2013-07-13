# commandline:
#  ldapsearch -xLLL -H <host> -b <base> <search>
import ldap
from eieldap import config


class Manager():
    """This a module to help with managing the eieldap using python"""

    def __init__(self,  config=config):
        self.connect(config)

    def __del__(self):
        self.disconnect()

    def connect(self, config):
        self.server = config.get("ldap", "server")
        self.dn = config.get("ldap", "dn")
        self.pw = config.get("ldap", "pw")
        self.base = config.get("ldap", "base")
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

    def find(self, base=None):
        if base is None:
            base = self.base
        result = self.connection.search_s(base,
                                          ldap.SCOPE_SUBTREE,
                                          "uid=*")
        if result:
            fields = [field for dn, field in result]
            return fields

    def find_one(self, attr, base=None):
        if base is None:
            base = self.base
        filterstr = "uid=" + attr["uid"]
        result = self.connection.search_s(base,
                                          ldap.SCOPE_SUBTREE,
                                          filterstr)
        if result:
            dn, fields = result[0]
            return fields
        else:
            return "Error, nothing found"


if __name__ == '__main__':
    manager = Manager(config)
    base = "ou=people," + manager.base
    r = manager.connection.search_s(base, ldap.SCOPE_SUBTREE, 'uid=*')
    # safe = ['leny', 'raduser', 'root', 'testuser']
    # cnt = 1
    # for dn, entry in r:
    #     if entry['uid'][-1] not in safe:
    #         # print cnt, 'Processing: ', repr(entry['uid'][-1])
    #         cnt += 1
    #         print repr(entry['uidNumber'][-1]), repr(entry['uid'][-1])
    # fields = manager.find_one({"uid": "moilwam"})
    print manager.find()
    print "All the people in " + manager.base
    # print fields
    # print fields["objectClass"]
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
