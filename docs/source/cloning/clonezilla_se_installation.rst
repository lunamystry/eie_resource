Clonezilla SE Installation
--------------------------
To install Clonezilla Server Edition (SE) you need to first install
the Diskless Remote Boot in Linux Server (DRBL Server).
Detailed instructions on how to go about this can be found on the
`drbl installation site`_ . What follows is an attempt at simplifying
the instructions for Dlab use. I assume knowledge of linux terminal
commands.

**Requirements :**

- Ubuntu 12.04 (LTS)

#. Get the key::

     sudo wget -q http://drbl.org/GPG-KEY-DRBL -O- | sudo apt-key add -

     The output from this should be `OK`.

#. Enable universe, mutliverse and restricted from Software Center
   sources. Open the Software Center. Then `Edit >> Software
   Sources...` then make sure universe, restricted and multiverse are
   checked (you will have to enter the support password). I think
   there will be a screenshot below.

   .. image:: screenshots/enabling_universe_multiverse_restricted.png
              :width: 500 px
              :alt: enabling universe, multiverse and restricted
              :align: center


#. Add the repository for downloading DRBL. This requires editing the
   `/etc/apt/sources.list`. Unfortunatetly I don't want to risk giving
   a single command for this like `cat blah >> /etc/apt/sources.list`
   so you will have to edit the file yourself. I like `vim` as my text
   editor but some prefer `gedit`. Paste the following at the end of
   the file `/etc/apt/sources.list`. This command will open `gedit` for
   you::

     gksudo gedit /etc/apt/sources.list

   then add this to the bottom::

     deb http://drbl.sourceforge.net/drbl-core drbl stable


#. Update your sources cache::

     sudo apt-get update

#. Install DRBL::

     sudo apt-get install drbl

.. note::

   if you're lazy like me, you can run `sudo apt-get update && sudo
   apt-get install drbl` instead of the last two steps separatetly.

Clonezilla SE configuration
---------------------------

Preliminary setup:
Make sure there is a `/home/support/Imaging/macadr-eth0.txt` and
`/home/support/Imaging/macadr-eth1.txt`. This will make life easier
later. I put the dlab computers from 1 to 42 in `macadr-eth0.txt` and
dlab computers 43 to 77 and all 10 Blab computers in
`macadr-eth1.txt`.

You need to have a list of MAC addresses for ALL the machines that
will EVER be cloned. If you get new machines, you have to run this
step again.

.. note::

   you only ever have to configure the server once. Unless you get new
   machines.

.. warning::

   Make sure both network cards are connected


To configure the DRBL server you run::

  sudo drblsrv -i

#. Do you want to install the network installation boot image....

   ANSWER: N

#. Do you want to use the serial console...

   ANSWER: N

#. Do you want to upgrade the operating systems?

   ANSWER: N

#. There are 2 kernels available for clients, which on do you prefere?

   ANSWER: 1

   the one "from this DRBL server"

.. _drblpush:

Running drblpush
~~~~~~~~~~~~~~~~

Now need to run drblpush, to actually, uhm... I guess configure. This will ask
you a whole lot of questions. Answers to the questions are given next in order
in which they appear in the clonezilla when this guide was written. A few
assumptions are made:

#. There is a file at `/home/dlabadmin/Imaging/eth0.txt` which contains the MAC
   addresses for DLAB1 to DLAB42 and 

#. there is a file at
   `/home/dlabadmin/Imaging/eth1.txt` which contains the MAC addresses for DLAB43
   to DLAB97

#. There is enough space on the Server running clonezilla (hotseat2 at the time
   of writting) to hold an image. An image is about the same size as the
   harddrive which is being cloned.

#. `/home/` is not mounted on a separate drive.

If those assumptions are met, you then need to run drblpush to do the actual, I
don't know what its called "configuring". From the terminal, type the following
command::

  sudo drblpush -i

This will prompt you for answers and here is cheatsheet. `You're welcome :-)`

#. Please enter DNS domain

   ANSWER: ug.eie.wits.ac.za

#. Please enter NIS/YP domain name

   ANSWER: hotseat2

#. Please enter the client hostname prefix

   ANSWER: dlab

#. ... Do you want to collect them?

   ANSWER: N

#. Do you want to let the DHCP service ... interface eth0 ?

   ANSWER: Y

#. Please tell me the file name which contains MAC addresses...

   ANSWER: /home/support/Imaging/eth0.txt

#. What initial number to use in the last set of digits...

   ANSWER 1

#. Do you want to let the DHCP service ... interface eth1 ?

   ANSWER: /home/support/Imaging/eth1.txt

#. What initial number to use in the last set of digits...

   ANSWER 43

#. In the system, there are 3 modes for diskless linux services...

   ANSWER: 2

#. In the system, there are 4 modes available for clonezilla...

   ANSWER: 1

#. When using clonezilla, which directory ... save the image

   ANSWER: /home/partimag

#. Do you want to set the pxelinux password for clients...

   ANSWER: N

#. Do you want to set boot prompt for clients?

   ANSWER: N

#. Do you want to use graphic background for PXE menu when clients
   boot?

   ANSWER: Y

#. Do you want to let DRBL server as a NAT server...

   ANSWER: N

#. Warning! If you go on, your firewall rules will be overwritten...

   ANSWER: Y

that should do it, you should now have a system ready to create and deploy
clones. Now the next question is how do you actually create and deploy a clone?
Checkout :doc:`index` for instruction on how to clone and deploy.

.. _drbl installation site: http://drbl.sourceforge.net/installation/
