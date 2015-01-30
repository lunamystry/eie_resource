**************************
General Installation Guide
**************************

Salt
----

Salt is the key to a simplified repeatable configuration. It is important to
understand basically how it works and to use it in all configurations which I
did since I make assumptions sometimes which I enforce with Salt.

What is Salt
------------

Salt is a configuration management tool which can be used to send commands to
machines or to maintain state of a machine. The Salt documentation site is one
of the most useful tools when learning salt with easy to follow tutorials and a
simple guide which provides examples.

There are two Salt masters, Backup (Backup.eie.wits.ac.za) and
Hotseat2 (Hotseat2.ug.eie.wits.ac.za). Backup is used for configuring servers
and Hotseat2 is for the Dlab machines.

There is a script in the eie_scripts on github which can be used to install
salt-master and salt-minion on SLES. It is a good idea to look through this
bash script to see what it is doing cause it may overide things which you may
not want it to such as proxy settings.


Once Salt is installed and LDAP server, you can configure any minion now. The
recognised minions are Babbage and EIELdap at the moment. The master is Backup
