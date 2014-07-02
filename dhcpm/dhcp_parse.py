"""
    a dhcp parser cause I can't find one that I like or works the way I want.
"""
__version__ = '0.1'


def extract_parameters(config_lines):
    """
        assume:
            * one parameter per line
            * comments are not important so just ignore
            * parameters are only at the top, so as soon as a line containing
              '{' is encountered or the end of the string is reached, then the
              extraction stops

        input: config string
        return: a list of parameters, Each parameter is a tuple with name and
                value.
    """
    parameters = []
    for line in config_lines:
        line.lstrip()
        if "{" in line:
            return parameters
        parameters = {"options": extract_options(config_lines)}

    return parameters


def extract_groups(config_lines):
    """
        Search for all lines that have '{' and return:
            {'parameters': [('name1', 'value1'), ('name2', 'value2')],
             'declarations': [declaration1, declaration2]}

        assume:
            * parameters always come first
            * declarations are like groups (name, values)

        input: config string
        return: a list of groups.
    """
    groups = []
    for line in config_lines:
        line.lstrip()
        group_lines = []
        in_group = False

        if "{" in line:
            name = line[:line.find("{")]
            in_group = True
        elif line.startwith("}"):
            sub_groups = extract_groups(group_lines)
            parameters = extract_parameters(group_lines)
            groups.append({"name": name,
                           "parameters": parameters,
                           "groups": sub_groups})
            in_group = False
        elif in_group:
                group_lines.append(line)

    return groups


def strip_comments(config_lines):
    """
        input: list of lines with comments
        return: list of lines without comments
    """
    uncommented = []
    for line in config_lines:
        if "#" in line:
            uncommented.append(line[:line.find("#")])
        else:
            uncommented.append(line)
    return uncommented


def extract_options(config_lines):
    """
        input: a list of lines from the config file
        return: a list of options from those lines
    """
    options = []
    for line in config_lines:
        line = line.lstrip()
        if line.startswith('option'):
            words = line.split(" ")
            name = words[1]
            values = "".join(words[2:]).split(',')
            options.append({"name": name, "values": values})
    return options


def subnets(config_lines):
    """
        assume:
            * subnets take up multiple lines and are not closed when are opened

        input: a list of lines
        return: a list of subnets with its options and groups
    """
    pass
