#!/bin/bash
cp /etc/openstack-dashboard/local_settings.py /etc/openstack-dashboard/local_settings.py.bak`date +%Y-%m-%d-%H:%M` 

sed -i "/^OPENSTACK_HOST/s/\"127.0.0.1\"/\"controller\"/g" /etc/openstack-dashboard/local_settings.py


sed -i "/^OPENSTACK_KEYSTONE_DEFAULT_ROLE/s/\"_member_\"/\"user\"/g" /etc/openstack-dashboard/local_settings.py

service apache2 reload
