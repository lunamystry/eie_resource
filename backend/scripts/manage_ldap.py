# commandline:
#  ldapsearch -xLLL -H <host> -b <base> <search>

import ldap
from ConfigParser import SafeConfigParser

class Manager():
    def __init__(self,config_location):
        self.connect(config_location)

    def __del__(self):
        self.disconnect()

    def connect(self,config_location):
        # You can pass any file-like object; if it has a name attribute,
        # that name is used when file format error messages are printed
        cfg = SafeConfigParser()
        cfg.read(config_location)
        self.server = cfg.get("ldap","server")
        self.dn = cfg.get("ldap","dn")
        self.pw = cfg.get("ldap","pw")
        self.base = cfg.get("ldap","base")

        con = ldap.initialize('ldap://'+self.server)
        con.simple_bind_s(self.dn,self.pw)
        r = con.search_s(self.base,ldap.SCOPE_SUBTREE)
        for dn,entry in r:
            print 'Processing',repr(dn)
        self.connection = con
        print self.validate_password("some","leny")
        self.change_password('cn=leny','pass','passing')

    def disconnect(self):
        self.connection.unbind()

    def print_exception(self,exception):
        args = exception.args[0] # Accessing using 0 feels wrong
        print "ERROR: Could not change password "
        print "INFO:", args["info"]
        print "DESC:", args["desc"]

    def change_password(self,uid,oldpw,newpw):
        """ User the python ldap function to change the passord
        of the user with the supplied uid"""
        try:
            self.connection.passwd_s(uid+self.base,oldpw,newpw)
        except Exception as e:
            self.print_exception(e)

    def validate_password(self,uid,password):
        return self.connection.compare_s('cn=leny,'+self.base, 'cn', password)

    def add_user(self,details):
        pass

    def add_machine(self,details):
        pass

    def delete_machine(self,dn):
        pass

    def delete_user(self,dn):
        pass

    def search(self,criteria):
        """The criteria is a ldap criteria """
        return self.connection.compare_s('cn=leny,dc=eie,dc=wits,dc=ac,dc=za', 'cn', 'leny')

if __name__ == '__main__':
    manager = Manager('../../config/ldap.cfg')
