"""
    a dhcp parser cause I can't find one that I like or works the way I want.
"""
__version__ = '0.1'

import re

# failover statements:
#   [ primary | secondary ];
#   address [ address ];
#   peer address [ address ];
#   port [ port-number ];
#   peer port [ port-number ];
#   max-response-delay [ seconds ];
#   max-unacked-updates [ count ];
#   mclt [ seconds ];
#   split [ index ];
#   hba [ colon-separated-hex-list ];
#   load balance max seconds [ seconds ];
#   max-lease-misbalance [ percentage ];
#   max-lease-ownership [ percentage ];
#   min-balance [ seconds ];
#   max-balance [ seconds ];
#
# range6
#   range [ dynamic-bootp ] low-address [ high-address]
#
# prefix6
#   prefix6 low-address high-address / bits;
#
KNOWN_PARAMETERS = [
    'adaptive-lease-time-threshold',
    'always-broadcast',
    'always-reply-rfc1048',
    'authoritative',
    'not authoritative',
    'boot-unknown-clients',
    'db-time-format',
    'ddns-hostname',
    'ddns-domainname',
    'ddns-rev-domainname',
    'ddns-update-style',
    'ddns-updates',
    'default-lease-time',
    'delayed-ack',
    'max-ack-delay',
    'do-forward-updates',
    'dynamic-bootp-lease-cutoff',
    'dynamic-bootp-lease-length',
    'filename',
    'fixed-address address,'
    'fixed-address6'
    'ip6-address',
    'get-lease-hostnames',
    'hardware',
    'host-identifier option',
    'infinite-is-reserved',
    'lease-file-name',
    'limit-addrs-per-ia',
    'dhcpv6-lease-file-name',
    'local-port',
    'local-address',
    'log-facility',
    'max-lease-time',
    'min-lease-time',
    'min-secs',
    'next-server',
    'omapi-port',
    'one-lease-per-client',
    'pid-file-name',
    'dhcpv6-pid-file-name',
    'ping-check',
    'ping-timeout',
    'preferred-lifetime',
    'remote-port',
    'server-identifier',
    'server-duid LLT',
    'server-duid EN',
    'server-duid LL',
    'server-name',
    'site-option-space',
    'stash-agent-options',
    'update-conflict-detection',
    'update-optimization',
    'update-static-leases',
    'use-host-decl-names',
    'use-lease-addr-for-default-route',
    'vendor-option-space'
    ]


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
    parameters = {}
    for line in config_lines:
        line = line.lstrip()
        if "{" in line:
            return parameters
        m = re.match(r'^('+'|'.join(KNOWN_PARAMETERS)+')', line)
        if m:
            parameters[m.group()] = line[m.end():].lstrip()

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
    in_group = False
    group_lines = []
    open_brace_count = 0
    for i, line in enumerate(config_lines):
        line = line.lstrip()
        if "{" in line and not in_group:
            name = line[:line.find("{")]
            in_group = True
        elif "{" in line and in_group:
            open_brace_count += 1
            group_lines.append(line)
        elif line.startswith("}") and open_brace_count == 0:
            parameters = extract_parameters(group_lines)
            group_options = extract_options(group_lines)
            sub_groups = extract_groups(group_lines)
            groups.append({"name": name,
                           "options": group_options,
                           "parameters": parameters,
                           "groups": sub_groups})
            in_group = False
            group_lines = []
        elif line.startswith("}"):
            open_brace_count -= 1
            group_lines.append(line)
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
    options = {}
    for line in config_lines:
        line = line.lstrip()
        if line.startswith('option'):
            words = line.split(" ")
            name = words[1]
            values = "".join(words[2:]).split(',')
            options[name] = values
    return options


def extract_allow_deny_ignore(config_lines):
    params = []
    for line in config_lines:
        line = line.lstrip()
        m = re.match(r'^(allow|deny|ignore)', line)
        if m:
            params.append({m.group(): line[m.end():].lstrip()})
    return params


if __name__ == '__main__':
    with open('data/test.conf', 'r') as f:
        for group in extract_groups(f.readlines()):
            print(group['groups'])
