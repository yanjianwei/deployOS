#!/bin/bash
service ntp restart
service mysql restart

su -s /bin/sh -c "glance-manage db_sync" glance
service glance-registry restart
service glance-api restart

service nova-api restart
service nova-cert restart
service nova-consoleauth restart
service nova-scheduler restart
service nova-conductor restart
service nova-novncproxy restart

su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf \
  --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron

service neutron-server restart
service nova-novncproxy restart


