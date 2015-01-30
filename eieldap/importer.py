import xlrd
import os

from .users import User, default_password

VALID_TITLES = ["Year Of Study", "Student Number", "First Name", "Last Name"]


def import_from_xls(workbook_name):
    """read file, create usernames and add user to ldap"""

    if not os.path.isfile(workbook_name):
        raise IOError(workbook_name + " could not be opened")

    class_list = xlrd.open_workbook(workbook_name)
    rows = extract(class_list)

    rows = strip_unused_rows(rows)
    rows = strip_unused_cols(rows)

    rows = add_usernames(rows)
    rows = add_passwords(rows)
    rows = make_yos_int(rows)

    for row in rows[1:]:
        User(username=row[4], 
             year_of_study=row[3], 
             password=row[5],
             student_number=row[2],
             first_name=str(row[0]),
             last_name=str(row[1])).create()


def extract(xl_file):
    """ goes through the xls file and extracts the user data """
    sh = xl_file.sheet_by_index(0)
    rows = []
    for row in range(sh.nrows):
        cols = []
        for col in range(sh.ncols):
            cols.append(sh.cell(row, col).value)
        rows.append(cols)
    return rows


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
        row[i] = int(float(row[i]))
    return rows


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
    headers.append("plainTextPassword")
    new_rows = []
    new_rows.append(headers)
    for row in rows[find_headers_row(rows) + 1:]:
        row.append(str(default_password))
        new_rows.append(row)
    return new_rows
