Cloning
*******

.. toctree::
   :maxdepth: 1

   clonezilla_se_installation
   clonezilla_live_how_to

Cloning, also called Imaging allows you to save an image (not like a camera
picture) of one computer (clone one computer) and restore it on other computers
quickly. This is done using Clonezilla in the Dlab.

This is a guide to clonezilla specific to the Dlab. Clonezilla is a partition
and disk imaging/cloning program. It comes in two flavors, Clonezilla Live and
Clonezilla Server Edition. Clonezilla Live comes as a CD. It is useful for
single machine cloning and deploying. Clonezilla Server Edition is installed on
a server. It is great for general cloning and deploying. This guide provides a
guide for Clonezilla Server Edition. If for some reason you feel you want to
know more about the live version, see :doc:`clonezilla_live_how_to`.

**Requirements :**

- Server with Ubuntu 14.04 (LTS)
- The MAC addresses of the computers you want to clone/deploy

The server should have clonezilla installed and configured (see
:doc:`clonezilla_se_installation` for installation and configuration
instructions)


Overview
~~~~~~~~

Cloning is pretty simple. You save one machine installation and the restore it
on another machine using clonezilla. Thats it! well, sort of. Here are the
grossly simplified steps.

*First you save an image*

  1. You first select the machine you want to clone.

  2. You tell the DRBL server that you want to use clonezilla to clone the
       machine

  3. You tell the machine you want to clone to boot from the network

  4. You wait for the cloning to finish

And Voila! you will have the image of the machine you just cloned in the
server.

*Secondly you restore the image*

  1. You first select the machine you want to restore to.

  2. You tell the DRBL server that you want to use clonezilla to restore the
       machine

  3. You tell the machine you want to restore to boot from the network

  4. You wait for the restoration to finish


Keep these simplified steps in mind as you go through more detailed
instructions.

Detailed Instructions (with pictures)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cloning is done using `dcs` in a terminal windows. Simply type::

  sudo dcs

and follow the instructions. To make your life easier, I provide screenshots.
In the interest of remaining DRY (Don't Repeat Yourself) I will mention now
that the instructions work the same for saving AND for restoring, just decide
what you want to do at the appropriate step (step 6).

Follow the screenshots

  1.
     .. image:: screenshots/cloning/1.png
              :width: 500 px
              :align: center

The first option is selected if you wish to select all the computers with the
MAC adresses in the server, skipping steps 2 and 3. The second one alows you
to select specific computer, forcing you to do steps 2 and 3.

  2.
     .. image:: screenshots/cloning/2.png
              :width: 500 px
              :align: center

  3.
     .. image:: screenshots/cloning/3.png
              :width: 500 px
              :align: center

Now that you have done steps 2 and 3 (or skipped them) you can move on to step
4, Start clonezilla. If you start it, remember to stop it when you're done
cloning. If you dont't stop it, the lab will not have internet and everyone
will hate you.

  4.
     .. image:: screenshots/cloning/4.png
              :width: 500 px
              :align: center

  5.
     .. image:: screenshots/cloning/5.png
              :width: 500 px
              :align: center

If you think you are an Expert, then stop reading this guide and do what you
know. Otherwise always choose beginner mode on the above screen.

  6.
     .. image:: screenshots/cloning/6.png
              :width: 500 px
              :align: center

This is the screen that basically differentiates between saving and restoring.
The first option is normally selected when saving, and the third option when
restoring the image. It is also possible to do just windows or just Ubuntu, I
have not done this so good luck with that.

  7.
     .. image:: screenshots/cloning/7.png
              :width: 500 px
              :align: center

  8.
     .. image:: screenshots/cloning/8.png
              :width: 500 px
              :align: center

  9.
     .. image:: screenshots/cloning/9.png
              :width: 500 px
              :align: center

  10.
     .. image:: screenshots/cloning/10.png
              :width: 500 px
              :align: center

  11.
     .. image:: screenshots/cloning/11.png
              :width: 500 px
              :align: center

  12.
     .. image:: screenshots/cloning/12.png
              :width: 500 px
              :align: center

  13.
     .. image:: screenshots/cloning/13.png
              :width: 500 px
              :align: center

And you're ALMOST done!

   .. image:: screenshots/cloning/14.png
              :width: 500 px
              :align: center

Now you need to switch on the computer you want to save or restore (depending
on what you selected in step 5) and press F12 (if using Dell) to select boot
options and the boot from NIC. This should show the client MAC address and then
show a blue screen then start saving/restoring.

Troubleshooting
~~~~~~~~~~~~~~~
Here are a few hints to help you clone the computers sucessfully::

  1. Easier if you keep a master computer which is clean and untouched to avoid
     transission of various software glitches of the clones.
  2. At times some computers may fail to clone, so it is recomended that you do
     a visual inspection and reclone those that fail, else resort to manual cloning.

To make sure that clonezilla is completely stopped, use::

    sudo drbl-all-service stop

If the computers are not seeing the image when you try to boot them from the
network, try::

    sudo drbl-all-service start

If that does not work, then try running `drblpush` again. See
:ref:`drblpush` for details.

