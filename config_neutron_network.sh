#!/bin/bash

pwd_dir=$(cd "$(dirname "$0")"; pwd)
. $pwd_dir/config_file.sh
. $pwd_dir/os_exception.sh

NEUTRON_CONF="/etc/neutron/neutron.conf"
ML2_INI="/etc/neutron/plugins/ml2/ml2_conf.ini"
L3_INI="/etc/neutron/l3_agent.ini"
DHCP_INI="/etc/neutron/dhcp_agent.ini"
METADATA_INI="/etc/neutron/metadata_agent.ini"

cp $NEUTRON_CONF $NEUTRON_CONF'.bak'`date +%Y-%m-%d-%H:%M`
cp $ML2_INI $ML2_INI'.bak'`date +%Y-%m-%d-%H:%M`
cp $L3_INI $L3_INI'.bak'`date +%Y-%m-%d-%H:%M`
cp $DHCP_INI $DHCP_INI'.bak'`date +%Y-%m-%d-%H:%M`
cp $METADATA_INI $METADATA_INI'.bak'`date +%Y-%m-%d-%H:%M`

NEUTRON_DB_PASSWORD=$1
NEUTRON_PASSWORD=$1
NOVA_PASS=$3
NEUTRON_SERVICE_AUTH_PASSWORD=$1
RABBIT_PASSWORD=$2 
NETWORK_TUN_IP=$4
METADATA_SECRET=$NEUTRON_PASSWORD
EXT_NET=$5

inidelete $NEUTRON_CONF database connection
iniset $NEUTRON_CONF DEFAULT verbose  True
iniset $NEUTRON_CONF DEFAULT rpc_backend  rabbit 
iniset $NEUTRON_CONF oslo_messaging_rabbit rabbit_host  controller
iniset $NEUTRON_CONF oslo_messaging_rabbit rabbit_userid  openstack  
iniset $NEUTRON_CONF oslo_messaging_rabbit rabbit_password $RABBIT_PASSWORD 
iniset $NEUTRON_CONF DEFAULT auth_strategy keystone

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

iniset $NEUTRON_CONF DEFAULT service_plugins router
iniset $NEUTRON_CONF DEFAULT allow_overlapping_ips True
iniset $ML2_INI ml2 type_drivers flat,vlan,gre,vxlan
iniset $ML2_INI ml2 tenant_network_types gre
iniset $ML2_INI ml2 mechanism_drivers openvswitch

iniset $ML2_INI ml2_type_flat flat_networks external 
iniset $ML2_INI ml2_type_gre tunnel_id_ranges  1:1000
iniset $ML2_INI securitygroup enable_security_group True
iniset $ML2_INI securitygroup enable_ipset True
iniset $ML2_INI securitygroup firewall_driver neutron.agent.linux.iptables_firewall.OVSHybridIptablesFirewallDriver

iniset $ML2_INI ovs local_ip $NETWORK_TUN_IP 
iniset $ML2_INI ovs bridge_mappings external:br-ex
iniset $ML2_INI agent tunnel_types gre

iniset $L3_INI DEFAULT interface_driver neutron.agent.linux.interface.OVSInterfaceDriver
iniset $L3_INI DEFAULT external_network_bridge br-ex 
iniset $L3_INI DEFAULT router_delete_namespaces  True

iniset $DHCP_INI DEFAULT interface_driver neutron.agent.linux.interface.OVSInterfaceDriver
iniset $DHCP_INI DEFAULT dhcp_driver neutron.agent.linux.dhcp.Dnsmasq
iniset $DHCP_INI DEFAULT dhcp_delete_namespaces True
iniset $DHCP_INI DEFAULT verbose  True

iniset $METADATA_INI DEFAULT auth_uri  http://controller:5000
iniset $METADATA_INI DEFAULT auth_url  http://controller:35357
iniset $METADATA_INI DEFAULT auth_region  RegionOne
iniset $METADATA_INI DEFAULT auth_plugin  password
iniset $METADATA_INI DEFAULT project_domain_id  default
iniset $METADATA_INI DEFAULT user_domain_id  default
iniset $METADATA_INI DEFAULT project_name  service
iniset $METADATA_INI DEFAULT username  neutron
iniset $METADATA_INI DEFAULT password  $NEUTRON_PASSWORD

inidelete $METADATA_INI DEFAULT auth_url 
inidelete $METADATA_INI DEFAULT auth_region 
inidelete $METADATA_INI DEFAULT admin_tenant_name 
inidelete $METADATA_INI DEFAULT admin_user 
inidelete $METADATA_INI DEFAULT admin_password 

iniset $METADATA_INI DEFAULT nova_metadata_ip controller
iniset $METADATA_INI DEFAULT metadata_proxy_shared_secret $METADATA_SECRET
iniset $METADATA_INI DEFAULT verbose True 

service openvswitch-switch restart

ovs-vsctl add-br br-ex
ovs-vsctl add-br br-ex $EXT_NET 

service neutron-plugin-openvswitch-agent restart
service neutron-l3-agent restart
service neutron-dhcp-agent restart
service neutron-metadata-agent restart

