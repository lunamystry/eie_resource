EIE resource frontend
=====================

Web front end for electrical engineering resource. 


Configuration
=============

Because I am lazy to figure out how to handle the following properly, I am
requiring that this be done:

The following files must exist:
/var/log/eie_resource.log  (must be writable by the application)
/etc/eieldap/logging_config.json
/etc/eieldap/resource.cfg
/etc/eieldap/eieldaprc

The naming is to try reflect the kind of configuration they have, and I think
of eieldap as a separate package from eie_resource thus two  configuration
files.

