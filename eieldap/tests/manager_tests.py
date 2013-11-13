"""
Making these tested automated is a little more thinking that I feel like
at the moment, they are thus completetly manual and an existing ldap must
be create with a configuration file in /etc/eieldap

in the form:

[ldap]
server: localhost
base: dc=eie,dc=wits,dc=ac,dc=za
dn: cn=admin,dc=eie,dc=wits,dc=ac,dc=za
pw: $ecre+

You must know whats in there and what the outputs should be
"""

import eieldap
import unittest
import tempfile
from eieldap.manager import Manager

class ManagerTestCase(unittest.TestCase):

    def test_find(self):
        """ Find everything in the directory """
        print
        print
        print "FIND EVERYTHING" + " -"*20
        manager = Manager()
        for item in manager.find():
            print str(item)

    # def test_find_filtered(self):
    #     print
    #     print
    #     print "FIND FILTERED" + " -"*20
    #     manager = Manager()
    #     # give only people
    #     print "\tAll dn must have ou=people"
    #     for item in manager.find(base="ou=people,"+manager.base):
    #         print str(item)

    #     # give only groups
    #     print
    #     print "\tAll dn must have ou=groups"
    #     for item in manager.find(base="ou=groups,"+manager.base):
    #         print str(item)

    #     # filter by uid
    #     print
    #     print "\tAll entries must have uid"
    #     for item in manager.find(filter_key="uid"):
    #         print str(item)

    #     # filter by cn
    #     print
    #     print "\tAll entries must have cn"
    #     for item in manager.find(filter_key="cn"):
    #         print str(item)

    def test_create(self):
        """ Can I create an entry"""
        print
        print
        print "CREATE A GROUP" + " -"*20
        manager = Manager()
        # I was interested in groups when I wrote this
        # look at the delist function
        dn = "cn=avengers,ou=groups,"+manager.base
        names = ['batman', 'ironman', 'hulk']
        members = []
        for name in names:
            member = "uid=" + name + ",ou=people," + manager.base
            members.append(member)

        attr = {"cn":"avengers",
                "objectClass":"posixGroup",
                "gidNumber": "123",
                "memberUID": names}
        manager.create(dn, attr)

    # def test_update(self):
    #     """ Can I update an entry"""
    #     print
    #     print
    #     print "UPDATE A GROUP" + " -"*20
    #     manager = Manager()
    #     # I was interested in groups when I wrote this
    #     # look at the delist function
    #     dn = "cn=avengers,ou=groups,"+manager.base
    #     names = ['batman', 'ironman', 'hulk']
    #     members = []
    #     for name in names:
    #         member = "uid=" + name + ",ou=people," + manager.base
    #         members.append(member)

    #     attr = {"cn":"avengers",
    #             "objectClass":"posixGroup",
    #             "gidNumber": "123",
    #             "memberUID": names}
    #     manager.update(dn, attr)

    # def test_delete(self):
    #     """ Can I delete entries """
    #     print
    #     print
    #     print "DELETE A GROUP CREATED BEFORE" + " -"*20
    #     manager = Manager()
    #     dn = "cn=avengers,ou=groups,"+manager.base
    #     manager.delete(dn)


if __name__ == "__main__":
    unittest.main()
