openldap2:
  pkg.installed

/tmp/slapd.conf.default:
  file.managed:
    - source: salt://ldapserver/slapd.conf.default
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: openldap2

/var/lib/ldap/DB_CONFIG:
  file.managed:
    - source: salt://ldapserver/DB_CONFIG
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: openldap2

/etc/openldap/schema/samba.schema:
  file.managed:
    - source: salt://ldapserver/samba.schema
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: openldap2

/tmp/default.ldif:
  file.managed:
    - source: salt://ldapserver/default.ldif
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: openldap2

configure:
  cmd.run:
    - name: slaptest -f /tmp/slapd.conf.default -F /etc/openldap/slapd.d; rcldap restart && slaptest -f /tmp/slapd.conf.default -F /etc/openldap/slapd.d
    - shell: /bin/bash
    - require:
      - file: /tmp/slapd.conf.default
      - pkg: openldap2

ldap:
  service:
    - running
    - enable: True
    - reload: True

add_default_entries:
  cmd.run:
    - name: ldapadd -x -D "cn=admin,dc=eie,dc=wits,dc=ac,dc=za" -w 'password' -f /tmp/default.ldif
    - shell: /bin/bash
    - require:
      - file: /tmp/default.ldif
      - service: salt-minion
      - pkg: openldap2
