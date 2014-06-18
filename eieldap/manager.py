# commandline:
#  ldapsearch -xLLL -H <host> -b <base> <search>
import ldap
import ldap.modlist
import time
import logging
from eieldap import config


logger = logging.getLogger("eieldap.manager")


class Manager():
    """This a module to help with managing the eieldap using python"""

    def __init__(self, config=config):
        self.connect(config)

    def connect(self, config):
        error_msg = ""
        for trycount in range(3):
            try:
                self.server = config.get("ldap", "server")
                self.dn = config.get("ldap", "dn")
                self.pw = config.get("ldap", "pw")
                self.base = config.get("ldap", "base")
                self.connection = ldap.initialize('ldap://'+self.server)
                self.admin_bind()
            except ldap.SERVER_DOWN:
                error_msg = "{0} seems to be down".format(self.server)
                logger.error("{0}, 2 sec wait...".format(error_msg))
                time.sleep(2)
            except ldap.LDAPError:
                error_msg = "Unable to connect to {0}".format(self.server)
                logger.error("{0}, 2 sec wait...".format(error_msg))
                time.sleep(2)
            else:
                logger.info("Connected to {0}".format(self.server))
                return
        raise EnvironmentError(error_msg)

    def admin_bind(self):
        self.dn = config.get("ldap", "dn")
        self.pw = config.get("ldap", "pw")
        self.connection.simple_bind_s(self.dn, self.pw)

    def admin_unbind(self):
        self.connection.unbind()

    def disconnect(self):
        self.admin_unbind()
        logger.info("disonnected to {}".format(self.server))

    def create(self, dn, fields):
        self.admin_bind()
        try:
            modlist = ldap.modlist.addModlist(fields)
            self.connection.add_s(dn, modlist)
        except ldap.ALREADY_EXISTS:
            error_msg = "{0} already exists".format(dn)
            logger.error(error_msg)
            raise ValueError(error_msg)
        except ldap.LDAPError as e:
            logger.error("An error occured while adding: {0}, {1}".format(
                str(fields), str(e)))
        raise RuntimeError("{} not create for reasons unknown".format(dn))

    def update(self, dn, new_attr):
        """ new_attr is a dictionary of values"""
        modlist = self.prepare_modlist(dn, new_attr)
        if modlist:
            try:
                self.admin_bind()
                self.connection.modify_s(dn, modlist)
            except ldap.LDAPError as e:
                logger.error("""\n\tCould not update user with dn: {0}
                                \tbecause: {1} \n\tmodlist: {2}""".format(
                    dn, e, str(modlist)))
                raise ValueError(str(e))
        raise RuntimeError("{} not updated for reasons unknown".format(dn))

    def prepare_modlist(self, dn, new_attr):
        attr = self.find_by_dn(dn)
        if attr is None:
            return None
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

    def dict_as_str(self, attr):
        return "\n".join(['%s\t: %s' % (k, v) for k, v in attr.items()])

    def delete(self, dn):
        try:
            self.connection.delete_s(dn)
            return True
        except ldap.NO_SUCH_OBJECT:
            logger.info("The dn: {0} was not there!".format(dn))
        except ldap.LDAPError as e:
            logger.debug(e)
        return False

    def change_password(self, dn, oldpw, newpw):
        try:
            self.admin_bind()
            self.connection.passwd_s(dn, None, newpw)
            return True
        except ldap.LDAPError as e:
            logger.debug("Password for {0} not changed - {1}".format(dn, e))
        return False

    def authenticate(self, dn, password):
        try:
            self.connection.bind_s(dn, password)
            return True
        except ldap.LDAPError as e:
            logger.debug("Couldn't authenticate {0} - {1}".format(dn, e))
        return False

    def find(self, base=None, filter_key="objectClass"):
        if base is None:
            base = self.base
        if filter_key is not "":
            filter_key = "(" + filter_key + "=*)"

        results = self.connection.search_s(base,
                                           ldap.SCOPE_SUBTREE,
                                           filter_key)
        users = []
        if results:
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
        list_fields = ['objectClass', 'mail', 'member', 'memberUid', 'host']
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
