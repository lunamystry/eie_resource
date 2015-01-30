import xlrd
import os
import re

from .users import User, default_password

VALID_TITLES = ["Username",
                "Password",
                "Year Of Study",
                "Student Number",
                "Primary Email Address",
                "First Name",
                "Last Name"]


def get_rows(workbook_name):
    """read file, and returns a list of the rows in the file processed"""

    if not os.path.isfile(workbook_name):
        raise IOError(workbook_name + " could not be opened")

    class_list = xlrd.open_workbook(workbook_name)
    rows = extract(class_list)

    rows = strip_unused_rows(rows)
    rows = strip_unused_cols(rows)

    rows = add_usernames(rows)
    rows = add_passwords(rows)
    rows = make_yos_int(rows)

    return rows


def add_from_xls(workbook_name, sync=False):
    """
        This will add users to the LDAP server configured in
        /etc/eie_config/eieldap.conf.

        If sync is True, then the users which are not in the xls file will be
        removed from the LDAP.
    """
    rows = get_rows(workbook_name)
    hdr_rows = rows[0]
    for row in rows[1:]:
        if not User.find(row[hdr_rows.index('Username')]):
            User(username=row[hdr_rows.index('Username')],
             year_of_study=row[hdr_rows.index('Year Of Study')],
             password=row[hdr_rows.index('Password')],
             student_number=row[hdr_rows.index('Student Number')],
             emails=[row[hdr_rows.index('Primary Email Address')]],
             hosts=['babbage.ug.eie.wits.ac.za'],
             first_name=str(row[hdr_rows.index('First Name')]),
             last_name=str(row[hdr_rows.index('Last Name')])).create()

    if sync:
        exceptions = ['root', 'dlabadmin', 'supervisor', 'admin']
        xls_usernames = get_usernames(rows)
        print(xls_usernames)
        for user in User.find():
            if user.username not in xls_usernames and \
                user.username not in exceptions:
                  User.delete(user.username)


def get_usernames(rows):
    """
    Returns a list of all usernames in the rows given.
    """
    hdr_rows = rows[0]
    usernames = []
    for row in rows[1:]:
        usernames.append(row[hdr_rows.index('Username')])
    return usernames


def extract(xl_file):
    """ goes through the xls file and extracts the user data """
    sh = xl_file.sheet_by_index(0)
    rows = []
    for row in range(sh.nrows):
        cols = []
        for col in range(sh.ncols):
            cols.append(remove_nonascii(sh.cell(row, col).value))
        rows.append(cols)
    return rows


def remove_nonascii(string):
    """
    This function removes all non-ascii characters from a string. I am really
    sorry to have to butcher people's names. I can't get my head around unicode
    in python2.7
    """
    s = ''.join([x for x in string if ord(x) < 128])
    return str(s)


def find_headers_row(rows):
    header_row = 0
    for row in rows:
        for title in VALID_TITLES:
            if title in row:
                return header_row
        header_row += 1


def strip_unused_cols(rows):
    valid_col_numbers = find_valid_col_numbers(rows)
    new_rows = []
    for row in rows:
        new_row = []
        for col_num in valid_col_numbers:
            new_row.append(str(row[col_num]))
        new_rows.append(new_row)
    return new_rows


def make_yos_int(rows):
    headers = rows[find_headers_row(rows)]
    i = headers.index('Year Of Study')
    for row in rows[1:]:
        row[i] = int(float(remove_nonint(row[i])))
    return rows


def remove_nonint(string):
    regex = re.compile('[^0-9\.]')
    return regex.sub('', string)

def find_valid_col_numbers(rows):
    titles = rows[find_headers_row(rows)]
    valid_col_numbers = []
    col_number = 0
    for title in titles:
        if title in VALID_TITLES:
            valid_col_numbers.append(col_number)
        col_number += 1
    return valid_col_numbers


def strip_unused_rows(rows):
    return rows[find_headers_row(rows):]


def add_usernames(rows):
    headers = rows[find_headers_row(rows)]
    headers.append("Username")
    rows[find_headers_row(rows)] = headers
    new_rows = []
    new_rows.append(headers)
    for row in rows[find_headers_row(rows) + 1:]:
        first_name = row[headers.index("First Name")]
        last_name = row[headers.index("Last Name")]
        username = last_name.lower().replace(" ", "") + first_name[0].lower()
        row.append(str(username))
        new_rows.append(row)
    return new_rows


def add_passwords(rows):
    headers = rows[find_headers_row(rows)]
    headers.append("Password")
    new_rows = []
    new_rows.append(headers)
    for row in rows[find_headers_row(rows) + 1:]:
        row.append(str(default_password))
        new_rows.append(row)
    return new_rows
