from eieldap import config
from eieldap.manager import Manager
from eieldap import logger


class Groups():
    def __init__(self, manager=None):
        if manager is None:
            manager = Manager(config)
        self.manager = manager
        self.basedn = "ou=groups," + self.manager.base
        self.keymap = {"dn": "id",
                       "cn": "name",
                       "member":"member"}
        self.inv_keymap = {}
        for k,v in self.keymap.items():
            self.inv_keymap[v] = k

    def save(self, attr):
        """ if the group exists update, if not create"""
        new_group = self.fix(attr, self.inv_keymap)
        dn = "cn=" + new_group["cn"] + "," + self.basedn
        group = self.manager.find_one(new_group, filter_key="cn")
        if group:
            logger.info("Updating group: " + str(new_group))
            self.manager.update(dn, new_group)
            return True
        else:
            new_group["objectClass"] = ["groupOfNames"]
            new_group["cn"] = str(new_group["cn"])
            new_group["member"] = "cn=road runner,ou=people,dc=example,dc=com"
            logger.info("creating group(dn): " + str(dn))
            logger.debug("creating group(attr): " + str(new_group))
            if 'dn' in new_group:
                del new_group['dn']
            self.manager.create(dn, new_group)
            return True
        return False

    def delete(self, name):
        """ Deletes a group """
        dn = "cn=" + name + "," + self.basedn
        #TODO: errors
        self.manager.delete(dn)

    def find(self):
        """ Returns all the people in the directory (think ldap)"""
        groups = self.manager.find(self.basedn, filter_key="cn")
        groups_list = []
        for group in groups:
            new_group = self.fix(group, self.keymap)
            groups_list.append(new_group)
        return groups_list

    def find_one(self, name=None, attr=None):
        """ Returns a single group """
        if name is not None:
            dn = "cn=" + name + "," + self.basedn
            group = self.manager.find_by_dn(dn)
            return self.fix(group, self.keymap)
        elif attr is not None:
            group = self.manager.find_one(attr, self.basedn, filter_key="cn")
            return self.fix(group, self.keymap)

    def fix(self, group, keymap):
        if group:
            new_group = {}
            for key in group.keys():
                try:
                    nkey = keymap[key]
                    new_group[nkey] = str(group[key])
                except KeyError:
                    logger.debug("key not mapped: " + key)
            return new_group
        else:
            return group
