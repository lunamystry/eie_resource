
Clonezilla Live
---------------

These instructions were taken from the "Complete Guide to Cloning" by
*Tebogo Mohotlhoane*

**Requirements :**

- Clonezilla live disc
- external hard disc.

.. note::

  Clonezilla will compress the device with the ratio 2.4:1 (approximated!). So to
  create an image of a device with 24GB of data, ensure that the external disc has at least
  10GB of free space.


#. Load the Clonezilla live disc onto the DVD-ROM drive. Plug in the external disc at
   this point.
#. Reboot the system and press F12 before the BIOS loads.
#. On the Boot Device Menu, select the 'Onboard or USB CD-ROM Drive' option. If
   the latter is not listed, go to 'System Setup > General > Boot Sequence' and check the
   box for the required option. Apply the changes, exit System Setup and repeat step 2.
#. Select each of the following options on the menus that appear:

   - Clonezilla live (default option)
   - en_US
   - don't touch keymap
   - Start_Clonezilla
   - device-image (since we want to create an image)
   - local_dev (we will be storing the image on the external disc. Ensure that the
     device is plugged in and connected to the system, then press 'Enter' to
     proceed)

.. note::

   The system drive containing the OS (sda – system device a?)
   will be listed first with all its partitions (a1, a5, a6 etc.). All other drives will
   come afterwards taking up the letters b, c, etc. If the system has only one
   drive (a), then the external disk will be sdb (sdb1 if it is not partitioned). An
   easier way is to use partition sizes.

   / Top_directory_in_the_local_device (the image can be moved
   afterwards)

#. To continue

  - Press 'Enter' to continue.
  - Beginner (simplest mode – sets best options as default on subsequent menus)
  - Note: can either
  - create an image of an entire disc as well as one or more partitions of a disc.
    For a disc:

     * select 'savedisk'

     * name the image being created. Use the convention shown as it will make
       identifying the image simpler.

     * select the disc to be cloned. Remember from point (vii) that our OSes are
       on sda. Press 'Enter' to proceed

  - confirm the procedure with 'y' followed by 'Enter'
  - once complete, press '0' (to shut the system down) or '1' (to reboot)
    followed by 'Enter'
    For partition imaging:

      * select 'saveparts'

      * name the image being created. Use the convention shown as it will
        make identifying the image simpler.

  - mark the partitions to be imaged using the spacebar to check the
    boxes. Press 'Enter' twice to continue

    * confirm the procedure with 'y' followed by 'Enter'

    * once complete, press '0' (to shut the system down) or '1' (to reboot)
      followed by 'Enter'
      remove the disc, close the tray and press 'Enter'
