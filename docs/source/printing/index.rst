Printing
********

The Dlab has 4 printers. Two *HP LaserJet P4015* (printer1 and printer2) and an
*HP LaserJet Enterprise 600 M601* (printer3) and an *HP LaserJet P2055dn*
(office printer). Printing access is controlled using cups and papercut which
run from Babbage. Printer1,2 and the office printer can do duplex (double
sided) printing. Printer3 cannot. I don't know why not, it's newer.

How it all works
----------------

You have printers, they connect via ethernet and the Wits network to Babbage.
Babbage has cups and papercut installed. Cups is there to share the printers
over the network and papercut is there to charge people for printing. The
printers are each configured to accept printing jobs only from Babbage and
simply discard printing from any other address either than 146.141.119.253.

.. note::

    Printer drivers are optional on Babbage but if you don't add them, duplex
    printing (double sided) will not work. This is possibly why printer 3 does
    not do duplex printing. Babbage might not have the correct driver
    installed.


Useful URLs
-----------

The papercut web interface can be accessed from:
`<http://babbage.ug.eie.wits.ac.za:9191>`_ .

The cups web interface to allow for viewing of printers and maybe copying
address of the printer for the purpose of adding it is:
`<http://babbage.ug.eie.wits.ac.za:631>`_


Papercut Installation
---------------------

I honestly cannot remember how I configured papercut, I remember the guide was
simple and straight foward though. I remember you have to create a separate
user for it with its own home directory. The `Papercut Knowledge base
<http://www.papercut.com/kb/Main/UserManual>`_ might provide help though.

Configuration
-------------

Once Papercut is installed, it runs from
`<http://babbage.ug.eie.wits.ac.za:9191>`_ and it has a user interface which
takes some getting used to. It allows do:

#. See who printed what and when and what the name of the document is

#. Change default or current credit

#. Print out a basic report of paper/printer usage

#. Sync LDAP users

And a whole lot more things. The whole configuration of papercut can be done
from the provided interface, one just needs to site and try out different
things and see what works.

The other important configuration for papercut to work is to tell the cups
printers that they should print via papercut. This is done by adding papercut
at the beginning of the address of the printer in the cups configuration file.
For example, the cups printers.conf entry for printer1 looks like this::

    <DefaultPrinter printer1>
        Info Dlab printer 1 with driver HP LaserJet p4015dn, hpcups 3.14.3
        Location Dlab
        DeviceURI papercut:socket://146.141.119.115:9100
        State Idle
        StateTime 1420611388
        Accepting Yes
        Shared Yes
        JobSheets none none
        QuotaPeriod 0
        PageLimit 0
        KLimit 0
        OpPolicy default
        ErrorPolicy abort-job
    </Printer>

.. note::

    The DeviceURI for printer1 would normally be: socket://146.141.119.115:9100
    but to use papercut, it becomes: papercut:socket://146.141.119.115:9100 

Here are the contents of a fully working printers.conf file for cups.

**printers.conf**

.. literalinclude:: printers.conf
