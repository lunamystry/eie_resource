****
LDAP
****

Introduction
============

I assume you know what LDAP is and if you come across a word you do
not understand, it is up to you to find out what it means. I have
provided links to a couple of the resources I have found most valuable
when starting out with LDAP. My favorite has to be Zytrax which
provides a more complete (in my opinion) introduction to LDAP.

These instructions are not meant to be followed blindly. Something can
be copied and pasted. There are some which will to be edited a little
as they were written and tested on ArchLinux.

Installation
============

This is depends on which Linux is used. I used ArchLinux and
installation was a simple `pacman -S openldap` this installed
everything that I needed. Ubuntu might be
`sudo apt-get install openldap` or you can use the Ubuntu software
center. SLES/openSuSE offers yast which is what I used for software
management and zypper when yast didn't want to listen to me. I have
not used zypper to instal openldap so I don't know what the package
is called.

Some external dependencies:
`sudo apt-get install python-dev libldap2-dev libsasl2-dev libssl-dev`

Initial configuration
=====================

OpenLDAP can be configured in two ways: slapd.conf and slapd.config.
Names look similar but they refer to two different configuration
methods. The first, slapd.conf is a configuration file which is
usually (depending on how you install openLDAP) found in
`/etc/openldap/slapd.conf`. This method of configuration is somewhat
easier to get started with when you are starting of with openLDAP.
The problem with it is that it is that with openLDAP 2.3 and above,
it is considered depreciated in favor of the second method,
slapd.config. slapd.config is storing the configurations in the LDAP
directory. This means that to change or add configurations, you have
to use operations like ldapadd and ldapmodify. These are the normal
operations you use when you are normally managing the LDAP directory.

I found starting of using slapd.conf and then migrating that into
slapd.config was an easier way to get started with configuration.
ArchLinux provides a nice simple example slapd.conf file which is
great for just playing around with the LDAP directory. Zytrax starts
of with the slapd.conf file method.

Here is the Zytrax configuration file edited for the eieldap. It
uses hdb instead of bdb for the backend. It allows anyone to be able
to authenticate which is needed for the webapp. It also allows people
in the itpeople group to be able to write all passwords.

.. literalinclude:: slapd.conf

Then you can adding a few test users. This is an ldif file that may
be used to add a test user. Notice that the root has to be added
first. This is `dc=eie,dc=wits,dc=ac,dc=za`.

.. literalinclude:: first.ldif

Now you start and add the first entries using::

  systemctl start slapd # rcslapd start on SLES
  ps ax | grep slapd # should show that the process is running


The output of ``ps ax | grep slapd`` should be something like::

  3402 ?        Ssl    0:00 /usr/sbin/slapd -u ldap -g ldap
  26364 pts/1    S+     0:00 grep slapd

The you can add the first entry using::

  ldapadd -x -D "cn=admin,dc=eie,dc=wits,dc=ac,dc=za" -w superdupersecret -f first.ldif

this uses the rootdn and rootpw that was set in the slapd.conf above.
To check if the entry was really added you can search for it::

  ldapsearch -x -D "cn=admin,dc=eie,dc=wits,dc=ac,dc=za" -w superdupersecret -b dc=eie,dc=wits,dc=ac,dc=za

In the interest of not reinventing the wheel, I end the introduction
and setup of the ldap here. To find out how to convert slapd.conf to
slapd.config or how to then add olcAccess and such, refer to:
`zytrax book <http://http://www.zytrax.com/books/ldap>`_

Phpldapadmin
============

Phpldapadmin is one of the recommended ldap management tools from
zytrax. It allows a vast majority of operations on the ldap. It also
has a very simple installation procedure.

Requirements
------------

* A working ldap directory
* A web server (Apache) configured to use PHP v5. PHP must be configured with:
   * PCRE support,
   * SESSION support,
   * GETTEXT support, (This gave me some issues on SLES, you install
     it with `yast -i php_gettext`)
   * LDAP support,
   * XML support

More information can be obtained from: `phpldapadmin requirements <http://phpldapadmin.sourceforge.net/wiki/index.php/PreRequisites>`_

Installation
------------
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

Cheatsheet
----------
