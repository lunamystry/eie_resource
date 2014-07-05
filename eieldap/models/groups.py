from ldap.dn import explode_dn
from eieldap import manager
from eieldap.models import users
import logging

logger = logging.getLogger('eieldap.models.groups')
BASEDN = "ou=groups," + manager.base
FROM_LDAP_MAP = {"cn": "name",
                 "gidNumber": "gid_number",
                 "description": "description",
                 "memberUid": "members"}
TO_LDAP_MAP = {}
for k, v in FROM_LDAP_MAP.items():
    TO_LDAP_MAP[v] = k


def save(group):
    """adds a new posix group to the LDAP directory"""
    if ("members" not in group
            or type(group['members']) is not list
            or len(group['members']) == 0):
        raise ValueError("You must give atleast one group member")
    if 'gid_number' not in group:
        raise ValueError("You must give a gid number")
    if 'name' not in group:
        raise ValueError("You must give a name")
    unfixed_group = dict(group)  # I don't want to be editing what I'm given
    unfixed_group['members'] = list(group['members'])
    for i, member_name in enumerate(unfixed_group["members"]):
        error_msg = "{} is not in the directory".format(member_name)
        if not users.find_one(member_name):
            logger.error(error_msg)
            raise ValueError(error_msg)

    fixed_group = convert(unfixed_group, TO_LDAP_MAP)
    dn = "cn=" + fixed_group["cn"] + "," + BASEDN
    existing_group = manager.find_one(fixed_group, filter_key="cn")
    if existing_group:
        manager.update(dn, fixed_group)
    else:
        fixed_group["objectClass"] = ["posixGroup"]
        fixed_group["cn"] = str(fixed_group["cn"])
        if 'dn' in fixed_group:
            del fixed_group['dn']
        manager.create(dn, fixed_group)


def find(name=None):
    """ Returns all the groups in the directory (think ldap)"""
    if name is not None:
        return find_one(name)
    groups = manager.find(BASEDN, filter_key="cn")
    return [convert(group, FROM_LDAP_MAP) for group in groups]


def find_one(name=None, group=None):
    """ Returns a single group """
    found_group = None
    if name is not None:
        dn = "cn=" + name + "," + BASEDN
        found_group = manager.find_by_dn(dn)

    if found_group:
        return convert(found_group, FROM_LDAP_MAP)

    if group is not None:
        fixed_group = convert(group, TO_LDAP_MAP)
        found_group = manager.find_one(fixed_group, BASEDN, filter_key="cn")

    if found_group:
        return convert(found_group, FROM_LDAP_MAP)


def delete(name=None, group=None):
    """ Deletes a group """
    existing_group = None
    if name is not None:
        dn = "cn=" + name + "," + BASEDN
        existing_group = manager.find_by_dn(dn)
    elif group is not None:
        fixed_group = convert(group, TO_LDAP_MAP)
        dn = "cn=" + fixed_group['cn'] + "," + BASEDN
        existing_group = manager.find_one(fixed_group, BASEDN, filter_key="cn")

    if existing_group:
        manager.delete(dn)


def add_member(group_name, member_username):
    """ should check it the member is the ldap then add them"""
    group = find_one(group_name)
    if not group:
        raise ValueError(str(group_name) + " does not exists")
    user = users.find_one(member_username)
    if not user:
        error_msg = "trying to add {0} to {1} but {0} is not in the directory".format(member_username, group_name)
        logger.error(error_msg)
        raise ValueError(error_msg)

    if user['username'] not in group['members']:
        group['members'].append(user['username'])
        save(group)


def remove_member(group_name, member_username):
    """ should check it the member is the ldap then add them"""
    group = find_one(group_name)
    if not group:
        raise ValueError(str(group_name) + " does not exists")

    if member_username in group['members']:
        if len(group['members']) == 1:
            raise ReferenceError("you cannot remove the last member of a group")
        group['members'].remove(member_username)
        save(group)
        logger.info("removed {0} from {1} group".format(member_username, group_name))
    else:
        logger.debug("{0} not found in {1} group".format(member_username, group_name))


def convert(group, keymap):
    if group:
        new_group = {}
        for key in group:
            if key in keymap:
                nkey = keymap[key]
                if type(group[key]) is list:
                    new_group[nkey] = group[key]
                else:
                    new_group[nkey] = str(group[key])
        return new_group
    else:
        return group
