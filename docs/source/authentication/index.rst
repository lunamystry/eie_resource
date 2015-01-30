Authentication
**************

Authentication in the lab uses the LDAP server. I am refering to logging into
Ubuntu, Window and the resource frontend. For details on how Papercut uses LDAP
for logging in see :doc:`printing <../printing/index>`.

Ubuntu
------

Ubuntu is authenticated directly from the LDAP server. This was configured by
following the instructions from the `Ubuntu Wiki`_ it does not use
the host name which is stored in the ldap to control which group in the ldap
can login to the machine (see nss_base_map on the `Ubuntu Wiki`_ under LDAP host
access authorization). This means everyone who is the ou=people can login to
the Ubuntu in the Dlab. This can be changed by adding::

    nss_base_passwd ou=people,dc=eie,dc=wits,dc=wits,dc=ac,dc=za?one?|(host=babbage.ug.eie.wits.ac.za)(host=\*)
    nss_base_shadow ou=people,dc=eie,dc=wits,dc=wits,dc=ac,dc=za?one?|(host=babbage.ug.eie.wits.ac.za)(host=\*)
    nss_base_group  ou=groups,dc=eie,dc=wits,dc=wits,dc=ac,dc=za?one

to the `/etc/ldap.conf` in the relevant section (see the `Ubuntu Wiki`_ if you
are not sure) it may be best to use salt for this kind of thing. The LDAP
server already has support for the host attribute as it uses the `nis.schema`.

.. _Ubuntu Wiki: https://help.ubuntu.com/community/LDAPClientAuthentication

Windows (Samba)
---------------

Windows authenticate to the LDAP using Samba. This is because Windows doesn't
play nice with Linux and generally is a pain to work with for these kind of
things.

Installing Samba
++++++++++++++++

Samba has to run on a Linux server, a SLES 11 server for this documentation. It
might work with OpenSUSE but I have not tried it. The installation and
configuration requires that a salt be working between the whatever master and
server which will run Samba. Also the :doc:`LDAP server <../ldap/index>` must
already have been configured. I assume :doc:`this guide <../ldap/index>` was
used for installing the LDAP server. I also assume the salt minion id for is
Babbage.

To start, you need to append the following to `/srv/salt/top.sls` in the salt
master::

    'Babbage':
        match: list
        samba

This basically says the minion with id Babbage should be given the samba
configuration when it asks.

Next the `/srv/salt/samba/init.sls` and `/srv/salt/samba/smb.conf` must exist
with the content given below. Once this requirement is met, the salt minion to
run Samba can be setup by running::

    sudo salt-call state.highstate

That will pull the configuration from the master and apply it to the minion.
Next the content of `/srv/salt/samba/init.sls` and `/srv/salt/samba/smb.conf`
are given.


**/srv/salt/samba/init.sls**

.. literalinclude:: samba/init.sls

**/srv/salt/samba/smb.conf**

.. literalinclude:: samba/smb.conf
