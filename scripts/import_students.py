#
# This script needs to be run from a directory where the eieldap can be found.

import argparse

from eieldap import xlstoldif

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        Convert an xls file in a specific format to an ldif file used. """)

    parser.add_argument('-i', '--input', dest='xls_url',
                        help='the path to the xls filename')
    parser.add_argument('-o', '--output', dest='ldif_url',
                        help='the path to the output ldif filename')

    args = parser.parse_args()
    xlstoldif.main(args.xls_url)
