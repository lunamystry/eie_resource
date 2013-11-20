Cloning
-------

Cloning, also called Imaging is where you copy one computer
installation from one computer to another. This is done using
Clonezilla in the Dlab. It allows us to create a single image and
deploy it all the machines quickly.

This is a guide to clonezilla specific to the Dlab. Clonezilla is a
partition and disk imaging/cloning program. It comes in two flavors,
Clonezilla Live and Clonezilla Server Edition. Clonezilla Live comes
as a CD. It is useful for single machine cloning and deploying.
Clonezilla Server Edition is installed on a server. It is great for
general cloning and deploying. This guide provides a guide for
Clonezilla Server Edition.

**Requirements :**

- Server with Ubuntu 12.04 (LTS)
- The MAC addresses of the computers you want to clone/deploy

The server should have clonezilla installed (see
:doc:`clonezilla_se_installation` for installation instructions)


Overview
~~~~~~~~

Cloning is pretty simple. You copy one machine installation to another
machine using clonezilla. Thats it, well, sort of. Here are the
simplified steps::

  1. You first select the machine you want to clone. You do this by
     selecting its MAC address from a list or previously configured
     MAC addresses.

  2. You tell the DRBL server that you want to use clonezilla to clone
     the machine

  3. You tell the machine you want to clone to boot from the network

  4. You wait for the cloning to finish

And Voila! you will have the image of the machine you just cloned in
the server.
Next you deploy this bad boy and here are the simplified steps::

  1. You first select the machine you want to deploy. You do this by
     selecting its MAC address from a list or previously configured
     MAC addresses.

  2. You tell the DRBL server that you want to use clonezilla to deploy
     the machine

  3. You tell the machine you want to deploy to boot from the network

  4. You wait for the deployment to finish

I copied and pasted the previous instructions :-).

Now for more detailed instructions.

Detailed Instructions (with pictures)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Cloning is done using `dcs` in a terminal windows. Simply::

  sudo dcs

and follow the instructions. To make your life easier, I provide
screenshots. In the interest of remaining DRY (Don't Repeat Yourself)
I will mention now that the instructions work the same for cloning and
for deploying, just decide what you want to do at the appropriate step.

Follow the screenshots

   .. image:: screenshots/cloning/1.png
              :width: 500 px
              :align: center

   .. image:: screenshots/cloning/2.png
              :width: 500 px
              :align: center

   .. image:: screenshots/cloning/3.png
              :width: 500 px
              :align: center

   .. image:: screenshots/cloning/4.png
              :width: 500 px
              :align: center

   .. image:: screenshots/cloning/5.png
              :width: 500 px
              :align: center

   .. image:: screenshots/cloning/6.png
              :width: 500 px
              :align: center

   .. image:: screenshots/cloning/7.png
              :width: 500 px
              :align: center

   .. image:: screenshots/cloning/8.png
              :width: 500 px
              :align: center

   .. image:: screenshots/cloning/9.png
              :width: 500 px
              :align: center

   .. image:: screenshots/cloning/10.png
              :width: 500 px
              :align: center

   .. image:: screenshots/cloning/11.png
              :width: 500 px
              :align: center

   .. image:: screenshots/cloning/12.png
              :width: 500 px
              :align: center

   .. image:: screenshots/cloning/13.png
              :width: 500 px
              :align: center

And you're done!

   .. image:: screenshots/cloning/14.png
              :width: 500 px
              :align: center

Now you go to the machine you want to clone, switch it, press F12 as
it starts and made the computer boot from the network.
Select the option shown below in the screenshot (thank you Kennedy):

   .. image:: screenshots/boot_from_network.jpg
              :width: 500 px
              :align: center

This will start cloning, it takes about 15 min to clone. Afterward you
follow the above steps again. The differences are:

#. Select the machine(s) you want to clone to instead of the one you
   want to clone
#. select restore-disk instead of save-disk.

This will give an extra
