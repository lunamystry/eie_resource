#
# This script needs to be run from a directory where the eieldap can be found.
import sys
sys.path.append('..')

import argparse

from eieldap import importer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        Add users to the ldap directory which is configured in
        /etc/eie_ldap/ldap.cfg """)

    parser.add_argument('-x', '--xlsfilename', dest='xlsfilename',
                        help='the path to the xls filename')
    parser.add_argument('-s', '--sync', action='store_true',
                        help='remove users which are not in the xls file')

    args = parser.parse_args()
    if args.xlsfilename:
        importer.add_from_xls(str(args.xlsfilename), args.sync)
    else:
        parser.print_usage()
