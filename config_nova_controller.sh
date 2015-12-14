#!/bin/bash

pwd_dir=$(cd "$(dirname "$0")"; pwd)
. $pwd_dir/config_file.sh
. $pwd_dir/os_exception.sh

NOVA_CONF="/etc/nova/nova.conf"

cp $NOVA_CONF $NOVA_CONF'.bak'`date +%Y-%m-%d-%H:%M`

NOVA_DB_PASSWORD=$1
RABBIT_PASSWORD=$2
LOCAL_IP=$3
NOVA_SERVICE_AUTH_PASSWORD=$1

iniset $NOVA_CONF DEFAULT verbose  True
iniset $NOVA_CONF DEFAULT rpc_backend  rabbit 
iniset $NOVA_CONF DEFAULT auth_strategy keystone  
iniset $NOVA_CONF DEFAULT my_ip $LOCAL_IP  
iniset $NOVA_CONF DEFAULT vncserver_listen $LOCAL_IP 
iniset $NOVA_CONF DEFAULT vncserver_proxyclient_address $LOCAL_IP

iniset $NOVA_CONF database connection mysql://nova:$NOVA_DB_PASSWORD@controller/nova

iniset $NOVA_CONF oslo_messaging_rabbit rabbit_host  controller
iniset $NOVA_CONF oslo_messaging_rabbit rabbit_userid  openstack  
iniset $NOVA_CONF oslo_messaging_rabbit rabbit_password $RABBIT_PASSWORD 
iniset $NOVA_CONF glance host  controller  
iniset $NOVA_CONF oslo_concurrency lock_path  /var/lib/nova/tmp  

inidelete $NOVA_CONF keystone_authtoken identity_uri
inidelete $NOVA_CONF keystone_authtoken admin_tenant_name 
inidelete $NOVA_CONF keystone_authtoken admin_user
inidelete $NOVA_CONF keystone_authtoken admin_password
inidelete $NOVA_CONF keystone_authtoken revocation_cache_time
iniset $NOVA_CONF keystone_authtoken auth_uri  http://controller:5000
iniset $NOVA_CONF keystone_authtoken auth_url  http://controller:35357
iniset $NOVA_CONF keystone_authtoken auth_plugin  password
iniset $NOVA_CONF keystone_authtoken project_domain_id  default
iniset $NOVA_CONF keystone_authtoken user_domain_id  default
iniset $NOVA_CONF keystone_authtoken project_name  service
iniset $NOVA_CONF keystone_authtoken username  nova 
iniset $NOVA_CONF keystone_authtoken password  $NOVA_SERVICE_AUTH_PASSWORD 

su -s /bin/sh -c "nova-manage db sync" nova

service nova-api restart
service nova-cert restart
service nova-consoleauth restart
service nova-scheduler restart
service nova-conductor restart
service nova-novncproxy restart
