Dlab documentation
******************

Here you will find documentation related to the Dlab. These instructions are
not meant to be followed blindly. There are included commands which can
sometimes be copied and pasted as is, some things though, may need some work
because they are obvious to me and what is obvious to me may not be obvious to
you. I have tried my best to make them as easy to use as I can though. As you
read through the documentation remember that to me, the thing is more important
than the name. 'A rose by any name is still a rose' so try Understand, DON'T
follow blindly.

If everything works as planned, this guide can guide you to configuring things
needed for the Dlab from scratch. 'Things needed for the Dlab' means the
Salt, Cloning, LDAP server, Samba and Printing.

How it all fits together
------------------------

You have salt, which is supposed to be used to control the lab on a daily
basis. :doc:`Salt <salt/index>` is to be used for simple things like: "There is
a booking tomorrow, could we please have such and such software installed".
Salt has the potential to make the lab work well without ever having to be
cloned again. :doc:`Cloning <cloning/index>` is a complement for Salt. It
allows one to copy one machine to another (basically). So what you can do is
install all the required software on one machine and then have copy it to all
the computers in the lab. 

Next you want to control who can login to the lab.  This is done using the
:doc:`LDAP server <ldap/index>`. The LDAP server is simply a storage of
usernames, passwords, home directories and other information about users of the
dlab. The LDAP server is then used to login to the computers. Ubuntu uses the
LDAP server directly and Windows goes through Samba, see
:doc:`authentication/index` for more details. The LDAP server is also used by
:doc:`Papercut <printing/index>` to authenticate users for printing.

The last thing is that as a :doc:`Dlab Administrator <admin/index>` there are
general things that you need to do. To try and help in this regard, the
:doc:`Resource webapp <webapp/index>` was created. This allows you to manage
users, groups, computers and provides useful links.


Table Of Content
----------------

.. toctree::
   :maxdepth: 2

   salt/index
   cloning/index
   ldap/index
   authentication/index
   printing/index
   admin/index
   webapp/index


Indices and tables
==================

#. :ref:`genindex`
#. :ref:`modindex`
#. :ref:`search`
