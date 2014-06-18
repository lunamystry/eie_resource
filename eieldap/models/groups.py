from eieldap import manager
from eieldap.models import users
import logging

logger = logging.getLogger('eieldap.models.groups')
BASEDN = "ou=groups," + manager.base
TO_LDAP_MAP = {"cn": "name",
               "gidNumber": "gid_number",
               "description": "description",
               "memberUid": "members"}
FROM_LDAP_MAP = {}
for k, v in TO_LDAP_MAP.items():
    FROM_LDAP_MAP[v] = k


def save(group):
    """adds a new posix group to the LDAP directory"""
    if ("members" not in group
            or type(group['members']) is not list
            or len(group['members']) == 0):
        raise ValueError("You must give atleast one group member")
    unfixed_group = dict(group)  # I don't want to be editing what I'm given
    unfixed_group['members'] = list(group['members'])
    for i, member_name in enumerate(unfixed_group["members"]):
        error_msg = "{} is not in the directory".format(member_name)
        if not users.find_one(member_name):
            logger.error(error_msg)
            raise ValueError(error_msg)

    fixed_group = convert(unfixed_group, FROM_LDAP_MAP)
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
    groups = manager.find(BASEDN, filter_key="cn")
    if name is not None:
        return find_one(name)
    groups_list = []
    for group in groups:
        if 'memberUid' in group:
            new_group = convert(group, TO_LDAP_MAP)
            groups_list.append(new_group)
        else:
            logger.error("{} does not have members".format(group['cn']))
    return groups


def find_one(name=None, group=None):
    """ Returns a single group """
    found_group = None
    if name is not None:
        dn = "cn=" + name + "," + BASEDN
        found_group = manager.find_by_dn(dn)

    if found_group:
        return convert(found_group, TO_LDAP_MAP)

    if group is not None:
        fixed_group = convert(group, FROM_LDAP_MAP)
        found_group = manager.find_one(fixed_group, BASEDN, filter_key="cn")

    if found_group:
        return convert(found_group, TO_LDAP_MAP)


# def delete(name=None, group=None):
#     """ Deletes a group """
#     existing_group = None
#     if name is not None:
#         dn = "cn=" + name + "," + BASEDN
#         existing_group = manager.find_by_dn(dn)
#     elif group is not None:
#         fixed_group = convert(group, FROM_LDAP_MAP)
#         dn = "cn=" + fixed_group['cn'] + "," + BASEDN
#         existing_group = manager.find_one(fixed_group, BASEDN, filter_key="cn")
#
#     if existing_group:
#         manager.delete(dn)
#
#
# def add_member(group_name, member_username):
#     """ should check it the member is the ldap then add them"""
#     group = find_one(group_name)
#     if not group:
#         raise ValueError(str(group_name) + " does not exists")
#     user = users.find_one(member_username)
#     if not user:
#         error_msg = "Trying to add : {0} to {1} but {0} is not in the directory".format(member_username, group_name)
#         logger.error(error_msg)
#         raise ValueError(error_msg)
#
#     if user['username'] not in group['members']:
#         group['members'].append(user['username'])
#         save(group)
#
#
# def remove_member(group_name, member_username):
#     """ should check it the member is the ldap then add them"""
#     group = find_one(group_name)
#     if not group:
#         raise ValueError(str(group_name) + " does not exists")
#
#     if member_username in group['members']:
#         if len(group['members']) == 1:
#             raise ReferenceError("You cannot remove the last member of a group")
#         group['members'].remove(member_username)
#         save(group)
#         logger.info("Removed {0} from {1} group".format(member_username, group_name))
#     else:
#         logger.debug("{0} not found in {1} group".format(member_username, group_name))


def convert(group, keymap):
    if group:
        new_group = {}
        for key in group.keys():
            if key in keymap:
                nkey = keymap[key]
                if isinstance(group[key], list):
                    new_group[nkey] = group[key]
                else:
                    new_group[nkey] = str(group[key])
        return new_group
    else:
        return group


# def next_gid_number(yos):
#     """returns the gid number based on the year of study given.
#     The following code applies:
#
#     yos - gid number - name
#      1  - 1000       - first year
#      2  - 2000       - second year
#      3  - 3000       - third year
#      4  - 4000       - fourth year
#         - M Eng      - 4500        - 4599        4500
#      5  - 5000       - postgrad
#      6  - 6000
#         - lecturers  - 6000        - 6099        6000
#         - admin      - 6100        - 6199        6100
#         - technical  - 6200        - 6299        6200
#         - postgrads  - 5000        - 5999        5000
#      7  - 7000       - machine
#
#     """
#     if yos not in range(1, 8):
#         logger.error("Tried to add out of range uid/yos")
#         raise ValueError("The Year of Study: " + str(yos) + " is out of range")
#
#     return yos*1000
