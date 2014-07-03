"""
    a dhcp parser cause I can't find one that I like or works the way I want.
"""
__version__ = '0.1'

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
# parameters
#   adaptive-lease-time-threshold [ percentage ];
#   always-broadcast [ flag ];
#   always-reply-rfc1048 [ flag ];
#   [authoritative | not authoritative];
#   boot-unknown-clients [ flag ];
#   db-time-format [ default | local ];
#   ddns-hostname [ name ];
#   ddns-domainname [ name ];
#   ddns-rev-domainname [ name ];
#   ddns-update-style [ style ];
#   ddns-updates [ flag ];
#   default-lease-time [ time ];
#   delayed-ack [count];
#   max-ack-delay [ microseconds ];
#   do-forward-updates [ flag ];
#   dynamic-bootp-lease-cutoff [ date ];
#   dynamic-bootp-lease-length [ length ];
#   filename [ "filename" ];
#   fixed-address address [, address ... ];
#   [ fixed-address6 ip6-address ];
#   get-lease-hostnames [ flag ];
#   hardware [ hardware-type ] [ hardware-address ];
#   host-identifier option [ option-name ] [ option-data ];
#   infinite-is-reserved [ flag ];
#   lease-file-name [ name ];
#   limit-addrs-per-ia [ number ];
#   dhcpv6-lease-file-name [ name ];
#   local-port [ port ];
#   local-address [ address ];
#   log-facility [ facility ];
#   max-lease-time [ time ];
#   min-lease-time [ time ];
#   min-secs [ seconds ];
#   next-server [ server-name ];
#   omapi-port [ port ];
#   one-lease-per-client [ flag ];
#   pid-file-name [ name ];
#
#   dhcpv6-pid-file-name [ name ];
#   ping-check [ flag ];
#   ping-timeout [ seconds ];
#   preferred-lifetime [ seconds ];
#   remote-port [ port ];
#   server-identifier [ hostname ];
#   server-duid LLT [ hardware-type timestamp hardware-address ];
#   server-duid EN enterprise-number enterprise-identifier;
#   server-duid LL [ hardware-type hardware-address ];
#   server-name [ name ];
#   site-option-space [ name ];
#   stash-agent-options [ flag ];
#   update-conflict-detection [ flag ];
#   update-optimization [ flag ];
#   update-static-leases [ flag ];
#   use-host-decl-names [ flag ];
#   use-lease-addr-for-default-route [ flag ];
#   vendor-option-space [ string ];


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


def extract_allow_deny_ignore(config_lines):
    params = []
    for line in config_lines:
        line = line.lstrip()
        if line.startswith('allow') or line.startswith('deny') or line.startswith('ignore'):
                words = line.split(" ")
                params.append({words[0]: words[1]})
    return params
