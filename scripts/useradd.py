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

    args = parser.parse_args()
    importer.import_from_xls(str(args.xlsfilename))
