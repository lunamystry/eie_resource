# commandline:
#  ldapsearch -xLLL -H <host> -b <base> <search>
import ldap
import ldap.modlist
from eieldap import config
from eieldap import logger

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
        modlist = ldap.modlist.addModlist(attr)
        try:
            self.connection.add_s(dn, modlist)
            return True
        except ldap.LDAPError as e:
            logger.debug(e)
        return False

    def update(self, dn, new_attr):
        """ Attr is a dictionary of values for a single thing"""
        modlist = self.prepare_modlist(dn, new_attr)
        try:
            self.connection.modify_s(dn, modlist)
            return True
        except ldap.LDAPError as e:
            logger.debug(e)
        return False

    def prepare_modlist(self, dn, new_attr):
        attr = self.find_by_dn(dn)
        try:
            del(attr["dn"])
        except KeyError:
            pass
        try:
            del(new_attr["dn"])
        except KeyError:
            pass
        for key in attr.keys():
            if key not in new_attr.keys():
                new_attr[key] = attr[key]
        modlist = ldap.modlist.modifyModlist(attr, new_attr)
        return modlist

    def delete(self, dn):
        self.connection.delete_s(dn)

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
        results = self.connection.search_s(base,
                                          ldap.SCOPE_SUBTREE,
                                          "uid=*")
        if results:
            users = []
            for result in results:
                result = self.de_list(result)
                users.append(result)
            return users

    def find_by_dn(self, strdn):
        dn = ldap.dn.str2dn(strdn)
        base = ldap.dn.dn2str(dn[1:])
        filterstr = ldap.dn.dn2str(dn[:1])
        result = self.connection.search_s(base,
                                          ldap.SCOPE_SUBTREE,
                                          filterstr)
        if result:
            fields = self.de_list(result[0])
            return fields

    def find_one(self, attr, base=None):
        if base is None:
            base = self.base
        filterstr = "uid=" + attr["uid"]
        result = self.connection.search_s(base,
                                          ldap.SCOPE_SUBTREE,
                                          filterstr)
        if result:
            fields = self.de_list(result[0])
            return fields

    def de_list(self, user):
        fields = []
        list_fields = ['objectClass', 'mail']
        dn, fields = user
        fields.update({"dn": [dn]})
        for key in fields:
            if key not in list_fields:
                fields[key] = fields[key][0]
        return fields


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
