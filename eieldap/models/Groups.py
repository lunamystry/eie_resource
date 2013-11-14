from eieldap import manager
from eieldap import logger
from eieldap.models import Users
import ldap


basedn = "ou=groups," + manager.base
keymap = {"cn": "name",
          "member": "members"}
inv_keymap = {}
for k, v in keymap.items():
    inv_keymap[v] = k


def find():
    """ Returns all the groups in the directory (think ldap)"""
    groups = manager.find(basedn, filter_key="cn")
    groups_list = []
    for group in groups:
        new_group = fix(group, keymap)
        groups_list.append(new_group)
    return groups_list


def find_one(name=None, attr=None):
    """ Returns a single group """
    group = None
    if name is not None:
        dn = "cn=" + name + "," + basedn
        group = manager.find_by_dn(dn)
    elif attr is not None:
        fixed_group = fix(attr, inv_keymap)
        group = manager.find_one(fixed_group, basedn, filter_key="cn")

    if group:
        group['member'] = get_names(group['member'])
        return fix(group, keymap)


def get_names(dn_list):
    for i, strdn in enumerate(dn_list):
        dn = ldap.dn.str2dn(strdn)
        _, name, _ = dn[0][0]
        dn_list[i] = name
    return dn_list


def save(group):
    """ if the group exists update, if not create"""
    logger.info(group)
    if "members" not in group or type(group['members']) is not list:
        raise TypeError("You must give atleast one group member")
    for i, member_name in enumerate(group["members"]):
        # TODO: member[i] = Users.find_one(member)["id"]
        group['members'][i] = "uid=" + member_name + "," + Users().basedn

    fixed_group = fix(group, inv_keymap)
    dn = "cn=" + fixed_group["cn"] + "," + basedn
    existing_group = manager.find_one(fixed_group, filter_key="cn")
    if existing_group:
        manager.update(dn, fixed_group)
        logger.info("Updated group: " + str(dn))
        return True
    else:
        fixed_group["objectClass"] = ["groupOfNames"]
        fixed_group["cn"] = str(fixed_group["cn"])
        if 'dn' in fixed_group:
            del fixed_group['dn']
        manager.create(dn, fixed_group)
        logger.info("Created group: " + str(dn))
        return True
    return False


def delete(name=None, group=None):
    """ Deletes a group """
    existing_group = None
    if name is not None:
        dn = "cn=" + name + "," + basedn
        existing_group = manager.find_by_dn(dn)
    elif group is not None:
        fixed_group = fix(group, inv_keymap)
        dn = "cn=" + fixed_group['cn'] + "," + basedn
        existing_group = manager.find_one(fixed_group, basedn, filter_key="cn")

    if existing_group:
        manager.delete(dn)


def add_member(group_name, member_name):
    """ should check it the member is the ldap then add them"""
    group = find_one(group_name)
    if not group:
        raise ValueError(str(group_name) + "Does not exists")
    user = Users().find_one(member_name)
    if not user:
        raise ValueError(str(user_name) + "Does not exists")


def fix(group, keymap):
    if group:
        new_group = {}
        for key in group.keys():
            try:
                nkey = keymap[key]
                if type(group[key]) is list:
                    new_group[nkey] = group[key]
                else:
                    new_group[nkey] = str(group[key])
            except KeyError:
                logger.debug("key not mapped: " + key)
        return new_group
    else:
        return group


def next_gid_number():
    pass
