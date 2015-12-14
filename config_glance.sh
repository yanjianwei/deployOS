#!/bin/bash

pwd_dir=$(cd "$(dirname "$0")"; pwd)
. $pwd_dir/config_file.sh
. $pwd_dir/os_exception.sh

GLANCE_API="/etc/glance/glance-api.conf"
GLANCE_REGISTRY="/etc/glance/glance-registry.conf"

cp $GLANCE_API $GLANCE_API'.bak'`date +%Y-%m-%d-%H:%M`
cp $GLANCE_REGISTRY $GLANCE_REGISTRY'.bak'`date +%Y-%m-%d-%H:%M`

GLANCE_DB_PASSWORD=$1
#REMOTE_PATH=$2

iniset $GLANCE_API DEFAULT verbose  True
iniset $GLANCE_API database connection mysql://glance:$GLANCE_DB_PASSWORD@controller/glance
iniset $GLANCE_API paste_deploy  flavor keystone

inidelete $GLANCE_API keystone_authtoken identity_uri
inidelete $GLANCE_API keystone_authtoken admin_tenant_name 
inidelete $GLANCE_API keystone_authtoken admin_user
inidelete $GLANCE_API keystone_authtoken admin_password
inidelete $GLANCE_API keystone_authtoken revocation_cache_time
iniset $GLANCE_API keystone_authtoken auth_uri  http://controller:5000
iniset $GLANCE_API keystone_authtoken auth_url  http://controller:35357
iniset $GLANCE_API keystone_authtoken auth_plugin  password
iniset $GLANCE_API keystone_authtoken project_domain_id  default
iniset $GLANCE_API keystone_authtoken user_domain_id  default
iniset $GLANCE_API keystone_authtoken project_name  service
iniset $GLANCE_API keystone_authtoken username  glance
iniset $GLANCE_API keystone_authtoken password  $GLANCE_DB_PASSWORD 
     
iniset $GLANCE_API DEFAULT notification_driver noop 

 
iniset $GLANCE_REGISTRY database connection mysql://glance:$GLANCE_DB_PASSWORD@controller/glance
inidelete $GLANCE_REGISTRY  keystone_authtoken identity_uri
inidelete $GLANCE_REGISTRY  keystone_authtoken admin_tenant_name 
inidelete $GLANCE_REGISTRY keystone_authtoken admin_user
inidelete $GLANCE_REGISTRY keystone_authtoken admin_password
inidelete $GLANCE_REGISTRY keystone_authtoken revocation_cache_time
iniset $GLANCE_REGISTRY keystone_authtoken auth_uri  http://controller:5000
iniset $GLANCE_REGISTRY keystone_authtoken auth_url  http://controller:35357
iniset $GLANCE_REGISTRY keystone_authtoken auth_plugin  password
iniset $GLANCE_REGISTRY keystone_authtoken project_domain_id  default
iniset $GLANCE_REGISTRY keystone_authtoken user_domain_id  default
iniset $GLANCE_REGISTRY keystone_authtoken project_name  service
iniset $GLANCE_REGISTRY keystone_authtoken username  glance
iniset $GLANCE_REGISTRY keystone_authtoken password  $GLANCE_DB_PASSWORD 
iniset $GLANCE_REGISTRY paste_deploy  flavor keystone
iniset $GLANCE_REGISTRY DEFAULT notification_driver noop 
 

su -s /bin/sh -c "glance-manage db_sync" glance
service glance-registry restart
service glance-api restart
rm -f /var/lib/keystone/keystone.db

echo "export OS_IMAGE_API_VERSION=2" | tee -a admin-openrc.sh demo-openrc.sh
source admin-openrc.sh
#mkdir /tmp/images
#wget -P /tmp/images http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img
#glance image-create --name "cirros-0.3.4-x86_64" --file $REMOTE_PATH/cirros-0.3.4-x86_64-disk.img \
 # --disk-format qcow2 --container-format bare --visibility public --progress

