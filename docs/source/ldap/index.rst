LDAP
****

LDAP stands for Light Directory Access Protocol and it started out as an
attempt to be a lighter version of the Directory Access Protocol. It is also
one of the weirdest things to configure followed in close second by Samba.

`Zytrax <http://www.zytrax.com/books/ldap>`_ has some of the best LDAP
documentation I have found in my time at the Dlab. I used the documentation
from to configure the eieldap in a way that works for me and I think is general
enough to be usable by others. This configuration can be found in on Backup or
you can contact me if you want a copy. I might still have one. The
configuration requires :doc:`Salt <../salt/index>` though.

In this document, I go though how to install and configure openldap for the
purposes of being used with Resource.eie.wits.ac.za, for Linux (Ubuntu,
Babbage) logins, Samba for Windows logins and Papercut for printing.

Requirements
------------

The whole installation and configuration uses Salt. The first that needs to be
done then is to have salt installed. Please refer to the :doc:`salt
<../salt/index>` documentation which I wrote for details on what salt is and
how to easly install it on SLES 11.

To do the installation, you will need two machines. The first machine is the
salt-master and the second is the salt-minion. The salt-minion is the machine
which will also be the LDAP server. Once you have the salt-master (I am
assuming Backup) and salt-minion (I am assuming EIEldap) installed and
configured to talk to each other, you can proceed with the installation and
configuration

Installation and configuration
------------------------------

There are two ways I have found to configure OpenLDAP. `Zytrax
<http://www.zytrax.com/books/ldap/ch6>`_ has an explanation of how both work. I
opted for the method of starting of using slapd.conf and then migrating that
into slapd.config.

Now, to install and configure OpenLDAP using Salt, you append the following to
the `/srv/salt/init.sls`::

    'EIEldap, testing':
        - match: list
        - ldapserver

This basically says, any minion with the id Babbage or testing should be given
the ldapserver state files.

Make sure that the files `/srv/salt/ldapserver/init.sls`,
`/srv/salt/ldapserver/DB_CONFIG`, `/srv/salt/ldapserver/samba.schema`,
`/srv/salt/ldapserver/default.ldif` and
`/srv/salt/ldapserver/slapd.conf.default` are all present on the master. You
can find the content of these files below.

Once you have made sure that all the files required are there with the correct
content. You simply have to run::

    salt-call state.highstate

On the minion with id EIEldap or testing to have it pull the configuration from
the master and apply it. You will then have to change the password for root in
samba. This is done with::

    sudo smbpasswd root

on the the minion which has Samba configured and everything should be fine.
Next the content of the required files for a working LDAP server are given.

**/srv/salt/ldapserver/DB_CONFIG**

.. literalinclude:: ldapserver/DB_CONFIG

**/srv/salt/ldapserver/init.sls**

.. literalinclude:: ldapserver/init.sls

**/srv/salt/ldapserver/default.ldif**

.. literalinclude:: ldapserver/default.ldif

**/srv/salt/ldapserver/slapd.conf.default**

.. warning::

    The you need to set the passwords in this file using some kind of hashing
    algorithm. You can use SSHA or MD5 (those are the 2 I have successfully
    used and are available on Linux. For example: 

    echo -n password | sha256sum

    then paste the output in the password lines (there are two) in the file.
    You will also have to paste the plaintext password in the deault.ldif file
    where it has `-w 'password'` replacing password with your password

.. literalinclude:: ldapserver/slapd.conf.default

**/srv/salt/ldapserver/samba.schema**

.. literalinclude:: ldapserver/samba.schema

PhpLDAPadmin
------------

Phpldapadmin is one of the recommended ldap management tools from zytrax. It
allows a vast majority of operations on the ldap. It also has a very simple
installation procedure. I never used this but you may find it useful.

Requirements
++++++++++++

* A working ldap directory
* A web server (Apache) configured to use PHP v5. PHP must be configured with:
   * PCRE support,
   * SESSION support,
   * GETTEXT support, (This gave me some issues on SLES, you install
     it with `yast -i php_gettext`)
   * LDAP support,
   * XML support

More information can be obtained from: `phpldapadmin requirements <http://phpldapadmin.sourceforge.net/wiki/index.php/PreRequisites>`_

PHPLDAP Installation
++++++++++++++++++++
To install you just need to:
  * `download <http://sourceforge.net/project/showfiles.php?group_id=61828>`_ the latest version
  * extract it and copy the resulting directory into your http docs
    root

Here is an example if you are using Ubuntu::

  wget http://sourceforge.net/projects/phpldapadmin/files/latest/download?source=files -O phpldapadmin
  tar xzvf phpldapadmin
  sudo mv phpldapadmin<version> /var/www/phpldapadmin
  # Edit /var/www/phpldapadmin/config/config.php to taste, the
  # comments guide you. Somethings you can just leave out and
  # phpldapadmin will figure them out
  firfox http://localhost/phpldapadmin

``<version>`` should be replaced by the latest version that has been
downloaded. Using TAB completion when entering the above commands
mean you don't have to worry about the version as it will completed
for you.

You should now be able to login using the full rootdn that you set in
the configuration. If you have not changed the slapd.conf file that
`phpldapadmin installation <http://phpldapadmin.sourceforge.net/wiki/index.php/Installation>`_

