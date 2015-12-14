#!/bin/bash

pwd_dir=$(cd "$(dirname "$0")"; pwd)
. $pwd_dir/os_exception.sh
. $pwd_dir/config_file.sh

fab -f host_env host_env
fab -f base_env base_env
fab -f identity identity 
fab -f image image 
fab -f compute compute 
fab -f network network 
fab -f dashboard dashboard 
CONTROLLER_NODE_IP=$(iniget config.ini CONTROLLER_NODE manage_ip )

echo "**********************************************"
echo " Congratulations,openstack deploy successful!"
echo " url: http://"$CONTROLLER_NODE_IP"/horizon"
echo " Any bug,please tell yanjianwei@fnic.cn"
echo "**********************************************"


