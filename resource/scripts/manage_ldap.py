# commandline:
#  ldapsearch -xLLL -H <host> -b <base> <search>

import ldap
from ConfigParser import RawConfigParser

# You can pass any file-like object; if it has a name attribute,
# that name is used when file format error messages are printed
cfg = RawConfigParser()
cfg.read('../resource.cfg')
server = cfg.get("ldap","server")
dn = cfg.get("ldap","dn")
pw = cfg.get("ldap","pw")

con = ldap.initialize('ldap://'+server)
con.simple_bind_s(dn,pw)
r = con.search_s('dc=eie,dc=wits,dc=ac,dc=za',ldap.SCOPE_SUBTREE)
for dn,entry in r:
    print 'Processing',repr(dn)
print con.compare_s('cn=leny,dc=eie,dc=wits,dc=ac,dc=za', 'cn', 'leny')
con.unbind()

def change_password():
    pass

def validate_password():
    pass

def add_user():
    pass

def add_machine():
    pass

def delete_machine():
    pass

def delete_user():
    pass

def search():
    pass

