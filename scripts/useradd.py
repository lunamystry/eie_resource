#
# This script needs to be run from a directory where the eieldap can be found.
import sys
sys.path.append('..')

import argparse

from eieldap import importer
from eieldap import users

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        Add users to the ldap directory which is configured in
        /etc/eie_ldap/ldap.cfg """)

    parser.add_argument('-x', '--xlsfilename', dest='xlsfilename',
                        help='the path to the xls filename')
    parser.add_argument('-s', '--sync', action='store_true',
                        help='remove users which are not in the xls file')
    parser.add_argument('-l', '--list', action='store_true',
                        help='list all the users in the ldap')
    parser.add_argument('--show', dest='show_username',
                        help='show the information for one user')
    parser.add_argument('--delete', dest='delete_username',
                        help='delete the information for one user')

    args = parser.parse_args()
    if args.xlsfilename:
        importer.add_from_xls(str(args.xlsfilename), args.sync)
    elif args.show_username:
        user = users.User.find(args.show_username)
        if user:
            print("{} ({} {})\nyos: {}\nhome: {}\nshell: {}\nuid: {}\ngid: {}".format(user.username,
                            user.first_name,
                            user.last_name,
                            user.year_of_study,
                            user.home_directory,
                            user.login_shell,
                            user.uid_number,
                            user.gid_number))
        else:
            print("User '{}' not found".format(args.username))
    elif args.delete_username:
        users.User.delete(args.delete_username)
    elif args.list:
        user_list = users.User.find()
        for user in user_list:
            print("{} ({} {}) - {}".format(user.username,
                                           user.first_name,
                                           user.last_name,
                                           user.year_of_study))
    else:
        parser.print_usage()
