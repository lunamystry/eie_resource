Resource Dlab Webapp
====================

The web front is an ambitious application to help manage the dlab. It started
out as an idea to manage just the users on the ldap server. Then I just got all
these ideas of what I can do with it that would be rather useful.

Installation
------------

The web app uses Python (Flask), Javascript (AngularJS), CSS (Bootstrap) and
HTML. It is hosted on `github`_ and that is where the code the be found
together with a README on how to install it and what configurations are needed.

.. _github : https://github.com/lunamystry/eie_resource

Setting dev environment
-----------------------

Its worth looking at the Openldap documentation for how ldap works.
Python-ldap has this `doc site`_

.. _doc site : http://www.python-ldap.org/docs.shtml


Design Overview
---------------

This is a simple overview of how I designed and structured the resource (I
still wish I could have called it iNqolobane).

RESTful API
-----------

The application has a sort of REST API providing access to the following
resources:

    users (requires rather weak authentication)

    computers

    bookings

    something

.. toctree::
   :maxdepth: 2
