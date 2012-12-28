# commandline:
#  ldapsearch -xLLL -H <host> -b <base> <search>

import ldap

server = 'eieldap.eie.wits.ac.za'
dn = "cn=admin,dc=eie,dc=wits,dc=ac,dc=za"
pw = "" # TODO: Find a better way to hold the password, read it from?
con = ldap.initialize('ldap://'+server)
con.simple_bind_s(dn,pw)
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

