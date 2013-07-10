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
            self.connection.passwd_s(dn, oldpw, newpw)
        except Exception as e:
            print e
            # self.print_exception(e)

    def authenticate(self, username, password):
        dn = username + self.base
        # first search for the username. Each username is unique for
        # each user.
        print dn
        self.connection.bind_s(dn, password)
        return True

    def add_user(self, details):
        pass

    def add_machine(self, details):
        pass

    def delete_machine(self, dn):
        pass

    def delete_user(self, dn):
        pass

    def search(self, criteria):
        """The criteria is a ldap criteria """
        return self.connection.compare_s('cn=leny,dc=eie,dc=wits,dc=ac,dc=za',
                                         'cn',
                                         'leny')

if __name__ == '__main__':
    manager = EIELdap('../config/ldap.cfg')
    r = manager.connection.search_s(manager.base, ldap.SCOPE_SUBTREE, 'uid=*')
    for dn, entry in r:
        # print dn
        # print 'Processing: ', repr(entry['uid'][-1])
        print entry, repr(entry['uid'][-1])
    print manager.authenticate('cn=Leonard Mbuli,ou=people,', "passing")
    # print manager.change_password('cn=Leonard Mbuli,ou=people,',
    #                               "pass",
    #                               "passing")

    # manager.change_password('uid=leny,ou=ug,'+manager.base,'pass', 'passing')
