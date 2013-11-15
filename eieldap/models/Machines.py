from eieldap import manager
from eieldap import logger


basedn = "ou=machines," + manager.base
keymap = {"uid": "name",
          "cn": ""}
inv_keymap = {}
for k, v in keymap.items():
    inv_keymap[v] = k


def find():
    """ Returns all the machines in the directory """
    machines = manager.find(basedn, filter_key="cn")
    machines_list = []
    for machine in machines:
        new_machine = fix(machine, keymap)
        machines_list.append(new_machine)
    return machines_list


def find_one(name=None, attr=None):
    """ Returns a single machine """
    machine = None
    if name is not None:
        dn = "cn=" + name + "," + basedn
        machine = manager.find_by_dn(dn)
    elif attr is not None:
        fixed_machine = fix(attr, inv_keymap)
        machine = manager.find_one(fixed_machine, basedn, filter_key="cn")

    if machine:
        machine['member'] = get_names(machine['member'])
        return fix(machine, keymap)


def get_names(dn_list):
    for i, strdn in enumerate(dn_list):
        dn = ldap.dn.str2dn(strdn)
        _, name, _ = dn[0][0]
        dn_list[i] = name
    return dn_list


def save(machine):
    """ if the machine exists update, if not create"""
    logger.info(machine)
    if "members" not in machine or type(machine['members']) is not list:
        raise TypeError("You must give atleast one machine member")
    for i, member_name in enumerate(machine["members"]):
        # TODO: member[i] = Users.find_one(member)["id"]
        machine['members'][i] = "uid=" + member_name + "," + Users.basedn

    fixed_machine = fix(machine, inv_keymap)
    dn = "cn=" + fixed_machine["cn"] + "," + basedn
    existing_machine = manager.find_one(fixed_machine, filter_key="cn")
    if existing_machine:
        manager.update(dn, fixed_machine)
        logger.info("Updated machine: " + str(dn))
        return True
    else:
        fixed_machine["objectClass"] = ["machineOfNames"]
        fixed_machine["cn"] = str(fixed_machine["cn"])
        if 'dn' in fixed_machine:
            del fixed_machine['dn']
        manager.create(dn, fixed_machine)
        logger.info("Created machine: " + str(dn))
        return True
    return False


def delete(name=None, machine=None):
    """ Deletes a machine """
    existing_machine = None
    if name is not None:
        dn = "cn=" + name + "," + basedn
        existing_machine = manager.find_by_dn(dn)
    elif machine is not None:
        fixed_machine = fix(machine, inv_keymap)
        dn = "cn=" + fixed_machine['cn'] + "," + basedn
        existing_machine = manager.find_one(fixed_machine, basedn, filter_key="cn")

    if existing_machine:
        manager.delete(dn)


def add_member(machine_name, member_username):
    """ should check it the member is the ldap then add them"""
    machine = find_one(machine_name)
    if not machine:
        raise ValueError(str(machine_name) + " does not exists")
    user = Users.find_one(member_username)
    if not user:
        error_msg = "Trying to add : {0} to {1} but {0} is not in "\
                    + "the directory".format(member_username, machine_name)
        logger.error(error_msg)
        raise ValueError(error_msg)

    if user['username'] not in machine['members']:
        machine['members'].append(user['username'])


def remove_member(machine_name, member_username):
    """ should check it the member is the ldap then add them"""
    machine = find_one(machine_name)
    if not machine:
        raise ValueError(str(machine_name) + " does not exists")

    if user['username'] in machine['members']:
        machine['members'].remove(member_username)


def fix(machine, keymap):
    if machine:
        new_machine = {}
        for key in machine.keys():
            try:
                nkey = keymap[key]
                if type(machine[key]) is list:
                    new_machine[nkey] = machine[key]
                else:
                    new_machine[nkey] = str(machine[key])
            except KeyError:
                logger.debug("key not mapped: " + key)
        return new_machine
    else:
        return machine
