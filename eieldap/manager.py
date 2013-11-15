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
        logger.debug(modlist)
        try:
            self.connection.add_s(dn, modlist)
            return True
        except ldap.LDAPError as e:
            logger.debug(e)
        return False

    def update(self, dn, new_attr):
        """ new_attr is a dictionary of values"""
        modlist = self.prepare_modlist(dn, new_attr)
        logger.debug(modlist)
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
        try:
            self.connection.delete_s(dn)
            return True
        except ldap.LDAPError as e:
            logger.debug(e)
        return False

    def change_password(self, dn, oldpw, newpw):
        try:
            self.connection.passwd_s(dn, None, newpw)
            return True
        except ldap.LDAPError as e:
            logger.debug(dn)
            logger.debug(e)

    def authenticate(self, dn, password):
        try:
            self.connection.bind_s(dn, password)
            return True
        except ldap.LDAPError as e:
            logger.debug(dn)
            logger.debug(e)
        return False

    def find(self, base=None, filter_key="objectClass"):
        if base is None:
            base = self.base
        if filter_key is not "":
            filter_key = "("+ filter_key + "=*)"

        results = self.connection.search_s(base,
                                           ldap.SCOPE_SUBTREE,
                                           filter_key)
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

    def find_one(self, attr, base=None, filter_key="uid"):
        if base is None:
            base = self.base
        filterstr = filter_key + "=" + attr[filter_key]
        result = self.connection.search_s(base,
                                          ldap.SCOPE_SUBTREE,
                                          filterstr)
        if result:
            fields = self.de_list(result[0])
            return fields

    def de_list(self, user):
        fields = []
        list_fields = ['objectClass', 'mail', 'member', 'memberUid']
        logger.debug("Keeping only: " + str(list_fields) + " as lists")
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
    # safe = ['leny', 'raduser', 'root', 'testuser', 'mbulil']
    # cnt = 1
    # for dn, entry in r:
    #     if entry['uid'][-1] not in safe:
    #         print dn
    #         # print cnt, 'Processing: ', repr(entry['uid'][-1])
    #         cnt += 1
    #         print repr(entry['uidNumber'][-1]), repr(entry['uid'][-1])
    #         manager.delete(dn)
    # fields = manager.find_one({"uid": "moilwam"})
    # print manager.find()
    # print "All the people in " + manager.base
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
    # print manager.authenticate('uid=moilwam,ou=people,dc=eie,dc=wits,dc=ac,dc=za', "0201672w")
    print manager.authenticate('uid=mbulil,ou=people,dc=eie,dc=wits,dc=ac,dc=za', "pass")
    # print manager.authenticate('uid=raduser,ou=people,dc=eie,dc=wits,dc=ac,dc=za', "pass")
    print manager.change_password('uid=mbulil,ou=people,dc=eie,dc=wits,dc=ac,dc=za',
                                  'passing',
                                  "pass")
    # manager.change_password('uid=leny,ou=ug,'+manager.base,'pass', 'passing')
