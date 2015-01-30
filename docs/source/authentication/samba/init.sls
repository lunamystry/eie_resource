samba:
  pkg.installed

/etc/samba/smb.conf:
  file.managed:
    - source: salt://samba/smb.conf
    - user: root
    - group: root
    - mode: 644
    - require:
      - pkg: samba

set ldap admin password:
  cmd.run:
    - name: smbpasswd -w 'password'
    - shell: /bin/bash
    - require:
      - pkg: samba

add dlabadmin:
  cmd.run:
    - name: smbpasswd -a dlabadmin -n
    - shell: /bin/bash
    - require:
      - pkg: samba

smb:
  service:
    - running
    - enable: True
    - reload: True

nmb:
  service:
    - running
    - enable: True
    - reload: True
