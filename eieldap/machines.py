"""
Saving a machine is done by samba, this is just to make it easy to get
and remove machines, if a machine is removed, it has to added by joining
it to the domain again.
"""
from eieldap import manager
import logging

logger = logging.getLogger(__name__)

basedn = "ou=machines," + manager.base
keymap = {"uid": "name"}  # the only thing that is unique
inv_keymap = {}
for k, v in keymap.items():
    inv_keymap[v] = k


def find():
    """ Returns all the machines in the directory """
    machines = manager.find(basedn, filter_key="uid")
    machines_list = []
    for machine in machines:
        new_machine = fix(machine, keymap)
        machines_list.append(new_machine)
    return machines_list


def delete(name=None, machine=None):
    """ Deletes a machine, can give either the name or the machine. If both are
    given, then the name is used"""
    existing_machine = None
    if name is not None:
        dn = "uid=" + name + "," + basedn
        existing_machine = manager.find_by_dn(dn)
    elif machine is not None:
        fixed_machine = fix(machine, inv_keymap)
        dn = "uid=" + fixed_machine['uid'] + "," + basedn
        existing_machine = manager.find_one(fixed_machine, basedn, filter_key="uid")

    if existing_machine:
        manager.delete(dn)
        return True
    return False


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
