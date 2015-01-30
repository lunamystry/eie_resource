Salt Configuration Management
*****************************


What is Salt
------------

Salt is the key to a simplified repeatable configuration. It is important to
understand basically how it works and to use it in all configurations which I
did since I make assumptions sometimes which I enforce with Salt. I used it to
configure the LDAP server, Samba and Resource. The `Salt documentation website
<http://docs.saltstack.com/en/latest/>`_ provides simple tutorials and
information on getting started with salt. This


Installation
------------

The latest installation instructions for Salt can be found the `Salt
installation page
<http://docs.saltstack.com/en/latest/topics/installation/index.html>`_. Here I
present how I installed Salt on SLES 11 service pack 1 and Ubuntu 14.04.
adapting these instructions.

.. warning::

  Make sure you install the same version of salt on all machines that work
  together. If the versions are different you get some weird behaviour
  sometimes. The instructions presented here gave the same version when I ran
  them.

Installation on SLES
~~~~~~~~~~~~~~~~~~~~

The folder `salt_bootstrap` in the `eie_scripts repo on github
<https://github.com/lunamystry/eie_scripts/>`_ has a script which can be used
to install salt-master and/or salt-minion on SLES 11. salt-master has to be
installed on Backup.eie.wits.ac.za and salt-minion has to be installed on
EIEldap, Babbage and Resource.

To use the script, you simply need to download and unzip the scripts::

    wget -O eie_scripts.zip https://github.com/lunamystry/eie_scripts/archive/master.zip eie_scripts.zip
    unzip -X eie_scripts.zip

Then inside the scripts directory you run salt bootstrap::

    cd eie_scripts-master/salt_bootstrap
    chmod +x boostrap.sh

Now depending on whether you want install a master or a minion, you will run::

    ./boostrap.sh sles master

or::

    ./boostrap.sh sles minion

The script was not written to be really that general. I wrote it to help me in
installing salt on a system that I know. In this regard, please don't just
assume it will work, have a look at what it does (like setting the proxy and
adding SLES 11.3 repos) by opening it. It really isn't that big.

Installation on Ubuntu
~~~~~~~~~~~~~~~~~~~~~~

Installation on Ubuntu is pretty straight foward, I simply followed the
instruction from the salt documentation. The commands are as follows::

    sudo add-apt-repository ppa:saltstack/salt
    sudo apt-get update
    sudo apt-get install salt-master salt-minion


Obviously if you want to just install a master or a minion you can leave out
the one you don't want.

Installation on Windows
~~~~~~~~~~~~~~~~~~~~~~~

Windows machines can only minions. The salt documentation provides the
installer for windows. Now I don't know enough about Powershell to have
commands to download and install salt on windows so this has to be done with
the help on clonezilla. You manually install the minion on one machine and then
clone that machine to the whole lab.

.. note::

   Note, don't set the minion id only the master in the configuration file.


Configuration
-------------

Once you have salt installed, configuration is easy. You don't have to do any
configuration for the master. An you simply need to tell the minions where to
find the master. This is done in the minion configuration file.

On linux (Ubuntu and SLES) this configuration file is found at
`/etc/salt/minion` on Windows, the configuration file is found at
`C:\\\\salt\\conf\\minion`. If either of these files, you need to find and set
the master line. For the Dlab machines, the master is `hotseat2` and for the
servers the master is `Backup`.

.. note::

  If you used the SLES installation script, the master will be automatically
  set as Backup.eie.wits.ac.za. You can change this by editing the default
  configuration file in the salt_boostrap folder.

Once you have save the minion configuration file you need to make sure that the
minion polls check the master at regular intervals for new configurations. A
simple way to do this on Linux is to use cron. You can refer `here
<http://docs.saltstack.com/en/latest/topics/tutorials/cron.html>`_ for more
details. 

.. warning::

    If you don't make the minion check the master at regular intervals, any
    changes you make will not go down to the minion.

The last thing that has to be done, it to accept the key from the minions on
the master. First you can review which minions need their keys approved::

    sudo salt-key list

Then you can accept all the keys with::

    sudo salt-key -A

Or accept only and individual key with (where minion_id is the id of the minion
whose key you want to accept::

    sudo salt-key -a minion_id

More detail if anything is not clear can found on the `salt documentaion
website <http://docs.saltstack.com/en/latest/topics/installation/index.html>`_.

How does it work
----------------

Salt has two basically ways in which it can be used. It can be used either
interactively or as a state manager. The interactive way is suitable for this
you want to do now and be done with. For example you want to shutdown all the
computers in the lab right now::

    sudo salt "*" system.shutdown

This command is run from the master and it will try to shutdown all minions of
that master. This uses salt modules and if you do a web search you search for
something like: "saltstack module add user windows". Salt documentation will
probably pop up and give you examples.

To use salt to manage a state you need to use salt state files. Salt state file
are files which are placed in `/srv/salt/` on the master and basically end with
`.sls`. A state is like a fact you want to be always true. Let us take Grub for
example::

    /etc/default/grub:
      file.managed:
        - source: salt://grub/grub_default.conf
        - user: root
        - group: root
        - mode: 644

    update-grub:
      cmd.run:
        - name: |
            update-grub
        - shell: /bin/bash
        - require:
          - file: /etc/default/grub

This is placed into a state file for Grub located in `/srv/salt/` and there
must be a folder called `/srv/salt/grub` which has
`/srv/salt/grub/grub_default.conf`. What the above state file basically says
is: "Make sure that the file `/etc/default/grub` looks exactly like the file
`/srv/salt/grub/grub_default.conf`. Then run the command `update-grub`." If the
the minion changes `/etc/default/grub`, those changes will be overidden by what
is in `/srv/salt/grub/grub_default.conf`.

The salt documentation is pretty easy to follow in their explanation of state
file `here
<http://docs.saltstack.com/en/latest/topics/tutorials/starting_states.html>`_.
It is at least better than anything I can come up with.

Example usage
-------------

*Forcing a minion to call the master*

To force a minion to check the master for new configuration, you run::

    sudo salt-call state.highstate

This is the same command which has to be called at regular intervals using a
cron job.

*Adding a new user*

Lets say there is an exam tomorrow and for some reason the LDAP server does not
work and you want to add a local use to DLAB43 and DLAB44::

    sudo salt "DLAB4[3,4]" user.add testuser 3000 3000 /home/ug/testuser /bin/bash

This command will add a new user called test user, with a UID and GID of 3000
and a home directory of /home/ug/testuser and a login shell /bin/bash. You can
find more details on this `here
<http://docs.saltstack.com/en/latest/ref/modules/all/salt.modules.useradd.html>`_.

*Shutdown all computers whose id ends with 'win8'*

Sometimes because you're still lazy learning salt, and don't know about pillars
yet, you might want to use the id of the minion to differentiate between the
Ubuntu and the windows 8 computers. If the ids have been set correctly, you can
choose to shutdown just the windows machines with::

    sudo salt "*win8" system.shutdown

As always, a link to the relevant salt documentation is `here
<http://docs.saltstack.com/en/latest/topics/targeting/globbing.html>`_.

*Running a script on a windows computer*

Lets say you have a script on a windows machine to join computers to the
domain.  You want to run this script but going to each computer on its own is
tedious and boring. Lets say the script is located at:
`C:\\\\Users\\dlabadmin\\Scripts\\run_join_domain.bat` on all minions and you
want to join all computers between DLAB60 and DLAB79::

    sudo salt 'DLAB[6,7][0-9]_win8' cmd.run 'C:\Users\dlabadmin\Scripts\run_join_domain.bat'


Known Issues
------------

While I think Salt is the best thing since clonezilla in helping to manage the
lab. It is not perfect and I didn't really get a chance to work with it fully.
It has some issues which I could not resolve. Some of the issues are:

#. Sometimes the minions don't respond to the master for no apparent reason.
   This I suspect is related to network connectivity. I think the computers
   might go to sleep sometimes and thus loose network connectivity. I did not
   check this. So I can't be sure.

#. Windows might not be configured to poll the server for new configurations.

#. The salt state files on Backup and on hotseat2 are not backed up. If either
   of these go down, they have to be done from scratch.
