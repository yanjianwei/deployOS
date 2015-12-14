#!/bin/bash

pwd_dir=$(cd "$(dirname "$0")"; pwd)
. $pwd_dir/config_file.sh
. $pwd_dir/os_exception.sh

NEUTRON_CONF="/etc/neutron/neutron.conf"
ML2_INI="/etc/neutron/plugins/ml2/ml2_conf.ini"
NOVA_CONF="/etc/nova/nova.conf"

cp $NEUTRON_CONF $NEUTRON_CONF'.bak'`date +%Y-%m-%d-%H:%M`
cp $ML2_INI $ML2_INI'.bak'`date +%Y-%m-%d-%H:%M`
cp $NOVA_CONF $NOVA_CONF'.bak'`date +%Y-%m-%d-%H:%M`

NEUTRON_DB_PASSWORD=$1
NEUTRON_PASSWORD=$1
NOVA_PASS=$3
NEUTRON_SERVICE_AUTH_PASSWORD=$1
RABBIT_PASSWORD=$2 
METADATA_SECRET=$NEUTRON_DB_PASSWORD

iniset $NEUTRON_CONF DEFAULT verbose  True
iniset $NEUTRON_CONF DEFAULT rpc_backend  rabbit 
iniset $NEUTRON_CONF DEFAULT auth_strategy keystone  
iniset $NEUTRON_CONF DEFAULT service_plugins router
iniset $NEUTRON_CONF DEFAULT allow_overlapping_ips True

iniset $NEUTRON_CONF DEFAULT notify_nova_on_port_status_changes True
iniset $NEUTRON_CONF DEFAULT notify_nova_on_port_data_changes True
iniset $NEUTRON_CONF DEFAULT nova_url http://controller:8774/v2

iniset $NEUTRON_CONF nova auth_url http://controller:35357
iniset $NEUTRON_CONF nova auth_plugin password
iniset $NEUTRON_CONF nova project_domain_id default
iniset $NEUTRON_CONF nova user_domain_id default
iniset $NEUTRON_CONF nova region_name RegionOne
iniset $NEUTRON_CONF nova project_name service
iniset $NEUTRON_CONF nova username nova
iniset $NEUTRON_CONF nova password $NOVA_PASS

iniset $NEUTRON_CONF database connection mysql://neutron:$NEUTRON_DB_PASSWORD@controller/neutron

iniset $NEUTRON_CONF oslo_messaging_rabbit rabbit_host  controller
iniset $NEUTRON_CONF oslo_messaging_rabbit rabbit_userid  openstack  
iniset $NEUTRON_CONF oslo_messaging_rabbit rabbit_password $RABBIT_PASSWORD 

inidelete $NEUTRON_CONF keystone_authtoken identity_uri
inidelete $NEUTRON_CONF keystone_authtoken admin_tenant_name 
inidelete $NEUTRON_CONF keystone_authtoken admin_user
inidelete $NEUTRON_CONF keystone_authtoken admin_password
inidelete $NEUTRON_CONF keystone_authtoken revocation_cache_time
iniset $NEUTRON_CONF keystone_authtoken auth_uri  http://controller:5000
iniset $NEUTRON_CONF keystone_authtoken auth_url  http://controller:35357
iniset $NEUTRON_CONF keystone_authtoken auth_plugin  password
iniset $NEUTRON_CONF keystone_authtoken project_domain_id  default
iniset $NEUTRON_CONF keystone_authtoken user_domain_id  default
iniset $NEUTRON_CONF keystone_authtoken project_name  service
iniset $NEUTRON_CONF keystone_authtoken username  neutron 
iniset $NEUTRON_CONF keystone_authtoken password  $NEUTRON_SERVICE_AUTH_PASSWORD 

iniset $NOVA_CONF DEFAULT network_api_class nova.network.neutronv2.api.API
iniset $NOVA_CONF DEFAULT security_group_api neutron
iniset $NOVA_CONF DEFAULT linuxnet_interface_driver nova.network.linux_net.LinuxOVSInterfaceDriver
iniset $NOVA_CONF DEFAULT firewall_driver nova.virt.firewall.NoopFirewallDriver

iniset $NOVA_CONF neutron url http://controller:9696
iniset $NOVA_CONF neutron auth_strategy keystone
iniset $NOVA_CONF neutron admin_auth_url http://controller:35357/v2.0
iniset $NOVA_CONF neutron admin_tenant_name service
iniset $NOVA_CONF neutron admin_username neutron
iniset $NOVA_CONF neutron admin_password $NEUTRON_PASSWORD


iniset $NOVA_CONF neutron service_metadata_proxy  True 
iniset $NOVA_CONF neutron metadata_proxy_shared_secret $METADATA_SECRET  

iniset $NEUTRON_CONF neutron firewall_driver nova.virt.firewall.NoopFirewallDriver
iniset $NEUTRON_CONF neutron service_metadata_proxy True 
iniset $NEUTRON_CONF neutron metadata_proxy_shared_secret $METADATA_SECRET

#ML2_CONF_INI
iniset $ML2_INI ml2 type_drivers flat,vlan,gre,vxlan
iniset $ML2_INI ml2 tenant_network_types gre
iniset $ML2_INI ml2 mechanism_drivers openvswitch

iniset $ML2_INI securitygroup enable_security_group True
iniset $ML2_INI securitygroup enable_ipset True
iniset $ML2_INI securitygroup firewall_driver neutron.agent.linux.iptables_firewall.OVSHybridIptablesFirewallDriver
iniset $ML2_INI ml2_type_gre tunnel_id_ranges  1:1000


su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf \
  --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron

service nova-api restart
service neutron-server restart

