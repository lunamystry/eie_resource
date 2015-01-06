# EIE resource frontend

Web front end for electrical engineering resource. 


## Requirements
mongodb - is used to store non-user items.

ldap - is used to store users, you thus must be able to connect to an ldap
server for testing. python-ldap is used.

smbencrypt - for generating LM and NT password hashes. This is usually provided
by a freeradius package, on ubuntu it is installed by 

    sudo apt-get install freeradius-utils python-ldap

## Installation
Python2.7 is needed to run the application. The requirements are listed in the 
requirements.txt file. It is recommended that the application be developed in a
virtualenvironment. The python-bootstrap script in the scripts folder can be 
used to install virtualenv.

Once the script is ran, it will create a $HOME/bin/virtualenvironments/env0 
virtualenv, the virtualenv installed in this can be used to create the
virtualenv for the application. With env0 activated, the following command will
create a virtualenv::

        virtualenv --distribute --python=2.7 --system-site-packages $HOME/.bin/virtualenvironments/resource

You install the required modules using::

        . $HOME/.bin/virtualenvironments/resource/bin/activate
        pip install -r requirements.txt


## Configuration

Because I am lazy to figure out how to handle the following properly, I am
requiring that this be done:

The following directory must exist:

        /var/log/eie_logs  (must be writable by the application)

The following files must exist:

        /etc/eie_config/logging_config.json
        /etc/eie_config/resource.cfg
        /etc/eie_config/eieldap.cfg

Examples are in the `config` directory of this
