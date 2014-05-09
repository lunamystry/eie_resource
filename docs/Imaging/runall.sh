#! /bin/bash
#sudo /opt/drbl/sbin/drblpush -i
#sudo /opt/drbl/sbin/drblpush -c /etc/drbl/drblpush.conf
sudo /opt/drbl/sbin/dcs
sudo ifdown eth0 && sudo ifup eth0
sudo ifdown eth1 && sudo ifup eth1
#sh ./wake_on_lan/dlab_1-42.sh
#sh ./wake_on_lan/dlab_43-77.sh
