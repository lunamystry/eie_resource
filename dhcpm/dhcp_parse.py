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
    pass


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
    pass


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


def options(config_lines):
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
    subnets = []
    for line in config_lines:
        line.lstrip()
        subnet = ""
        netmask = ""
        subnet_options = []
        subnet_lines = []
        in_subnet_config = False
        if line.startswith("subnet") and "{" in line:
            if in_subnet_config:
                raise SyntaxError("we don't support subnet in a subnet")
            words = line.split(" ")
            subnet = words[1]
            netmask = words[3]
            in_subnet_config = True
        elif line.startwith("}"):
            subnet_options = options(subnet_lines)
            subnets.append({"subnet": subnet,
                            "netmask": netmask,
                            "options": subnet_options})
            in_subnet_config = False
        else:
            subnet_lines.append(line)
    return subnets
