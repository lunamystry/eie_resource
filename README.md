EIE resource frontend
=====================

Web front end for electrical engineering resource. 


Configuration
=============

Because I am lazy to figure out how to handle the following properly, I am
requiring that this be done:

The following directory must exist:

        /var/log/eie_logs  (must be writable by the application)

The following files must exist:

        /etc/eie_config/logging_config.json
        /etc/eie_config/resource.cfg
        /etc/eie_config/eieldaprc

The naming is to try reflect the kind of configuration they have, and I think
of eieldap as a separate package from eie_resource thus two  configuration
files.

