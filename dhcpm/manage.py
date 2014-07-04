#! /usr/bin/env python
"""
    manage.py

    A script to manage machines in the ug dhcpd.conf
"""

import argparse
import re


class Host():
    def __init__(self, name, mac, ipv4, owner, remove_date, admin, comment):
        '''
            input
                name: of the machine
                mac: the MAC address of the machine
                ipv4: the ip address of the machine
                owner: the owner of the machine
                remove_date: the date when the machine can be removed
                admin: initials of the person adding the machine
                comment: a general comment about the addition
        '''
        self.name = name
        self.mac = mac
        self.ipv4 = ipv4
        self.owner = owner
        self.remove_date = remove_date
        self.admin = admin
        self.comment = comment


def add_host(filename=None):
    if filename:
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                name, value = re.search(r'(name):\s()').groups()
                print(line)
    else:
        name = raw_input("name: ")
        mac = raw_input("mac: ")
        ipv4 = raw_input("ipv4: ")
        owner = raw_input("owner: ")
        remove_date = raw_input("remove_date: ")
        admin = raw_input("admin: ")
        comment = raw_input("comment: ")
        new_host = Host(name, mac, ip, owner, remove_date, admin, comment)
        print(new_host)


def remove_host(host):
    pass


def update_host(host):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Manage the ug dhcpd.conf file")
    parser.add_argument('filename',
                        help="location of the dhcpd.conf file")
    parser.add_argument('-a', '--add', action='store_true',
                        help="file which has host information")
    parser.add_argument('-u', '--update', action='store_true',
                        help="file which has host information")
    parser.add_argument('-r', '--removed', action='store_true',
                        help="file which has host information")
    parser.add_argument('-f', '--file', action='store',
                        help="file which has host information")

    args = parser.parse_args()
    if args.add:
        add_host(args.file)
