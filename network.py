#!/usr/bin/env python
# encoding: utf-8
from fabric_env import *

neutron_db_pwd=read_cfg_file('NEUTRON','db_password')

@task
@roles('controller')
def install_contollernode():
    #with cd(remote_path),hide('stdout', 'stderr'):
    with cd(remote_path):
        run('apt-get install neutron-server neutron-plugin-ml2 python-neutronclient -y')

@task
@roles('controller')
def config_controllernode():
    config_file_sh="config_file.sh"
    config_neutron_controller_sh="config_neutron_controller.sh"
    
    put('%s'%config_neutron_controller_sh, '%s'%remote_path, mode=777)
    put('%s'%config_file_sh, '%s'%remote_path, mode=777)
 
    rabbit_pwd=read_cfg_file("RABBITMQ",'password')
    nova_pwd=read_cfg_file("NOVA",'db_password')
    
    with cd(remote_path):
        run('%s/%s %s %s %s'%(remote_path,config_neutron_controller_sh,neutron_db_pwd,rabbit_pwd,nova_pwd))
        run('rm %s'%config_neutron_controller_sh)

@task
@roles('controller')
def config_image():
    config_file_sh="config_file.sh"
    cirros="cirros-0.3.4-x86_64-disk.img"
    os_exception="os_exception.sh"    
    
    put('%s'%config_file_sh, '%s'%remote_path, mode=777)
    put('%s'%cirros, '%s'%remote_path, mode=777)
    put('%s'%os_exception, '%s'%remote_path, mode=777)
    
    with cd(remote_path):
        run('source admin-openrc.sh && glance image-create --name "cirros-0.3.4-x86_64" --file ./cirros-0.3.4-x86_64-disk.img --disk-format qcow2 --container-format bare --visibility public --progress')

@task
@roles('controller')
def check_image():
    with cd(remote_path):
	run('source admin-openrc.sh && glance image-list')
 
@task
@roles('network')
def config_networknode():
    config_file_sh="config_file.sh"
    config_neutron_network_sh="config_neutron_network.sh"
    os_exception="os_exception.sh"   
    restart_network_sh="restart_network.sh"   
  
    put('%s'%config_neutron_network_sh, '%s'%remote_path, mode=777)
    put('%s'%config_file_sh, '%s'%remote_path, mode=777)
    put('%s'%os_exception, '%s'%remote_path, mode=777)
    put('%s'%restart_network_sh, '%s'%remote_path, mode=777)
    
    rabbit_pwd=read_cfg_file("RABBITMQ",'password')
    nova_pwd=read_cfg_file("NOVA",'db_password')
    net_tun_ip=read_cfg_file("NETWORK_NODE",'manage_ip')
    ext_net=read_cfg_file("NETWORK_NODE",'ext_net') 
    ext_net_ip=read_cfg_file("NETWORK_NODE",'ext_net_ip')
    ext_net_netmask=read_cfg_file("NETWORK_NODE",'ext_net_netmask')
     
    #with cd(remote_path),hide('stdout', 'stderr'):
    with cd(remote_path):
        run('ifconfig %s up'%ext_net)
        run('ifconfig %s %s netmask %s'%(ext_net,ext_net_ip,ext_net_netmask))
        run('%s/%s %s %s %s %s %s'%(remote_path,config_neutron_network_sh,neutron_db_pwd,rabbit_pwd,nova_pwd,net_tun_ip,ext_net))
        run('rm %s'%config_neutron_network_sh)
        run('rm %s'%config_file_sh)
        run('ovs-vsctl add-port br-ex %s'%ext_net)

@task
@roles('network')
def install_networknode():
    #with cd(remote_path),hide('stdout', 'stderr'):
    with cd(remote_path):
        run('echo "net.ipv4.ip_forward=1">>/etc/sysctl.conf')
        run('echo "net.ipv4.conf.all.rp_filter=0">>/etc/sysctl.conf')
        run('echo "net.ipv4.conf.default.rp_filter=0">>/etc/sysctl.conf')
        run('sysctl -p')
        run('apt-get install neutron-plugin-ml2 neutron-plugin-openvswitch-agent \
  neutron-l3-agent neutron-dhcp-agent neutron-metadata-agent -y')

@task
@roles('compute')
@parallel
def install_computenode():
    #with cd(remote_path),hide('stdout', 'stderr'):
    with cd(remote_path):
        run('echo "net.ipv4.conf.all.rp_filter=0">>/etc/sysctl.conf')
        run('echo "net.ipv4.conf.default.rp_filter=0">>/etc/sysctl.conf')
        run('echo "net.bridge.bridge-nf-call-iptables=1">>/etc/sysctl.conf')
        run('echo "net.bridge.bridge-nf-call-ip6tables=1">>/etc/sysctl.conf')
        run('sysctl -p')
        run('apt-get install neutron-plugin-ml2 neutron-plugin-openvswitch-agent -y')

@task
@roles('controller')
def init_neutrondb():
    with cd(remote_path),prefix('source admin-openrc.sh'):
        run('openstack user create --password-prompt neutron')
        run('openstack role add --project service --user neutron admin')
        run('openstack service create --name neutron \
             --description "OpenStack Network service" network')
        run('openstack endpoint create \
             --publicurl http://controller:9696 \
             --adminurl http://controller:9696 \
             --internalurl http://controller:9696 \
             --region RegionOne \
             network')
     
@task
@roles('controller')
def create_networkdb():
    db_ip="localhost"
    db_pwd=read_cfg_file('DATABASE','root_password')
    grant_privailege_sh="grant_privaileges.sh"      
    db_name="neutron"
 
    with cd(remote_path):
         run('mysql -uroot -p%s -h%s -e "DROP DATABASE IF EXISTS %s;" '%(db_pwd,db_ip,db_name))
         run('mysql -uroot -p%s -h%s -e "CREATE DATABASE %s;" '%(db_pwd,db_ip,db_name))
    put('%s'%grant_privailege_sh, '%s'%remote_path, mode=777)
    with cd(remote_path):
        run('%s/%s %s %s %s %s'%(remote_path,grant_privailege_sh,db_pwd,db_ip,neutron_db_pwd,db_name))
        run('rm %s/%s'%(remote_path,grant_privailege_sh))

@task
@roles('compute')
def config_computenode():
    config_file_sh="config_file.sh"
    config_neutron_compute_sh="config_neutron_compute.sh"
    put('%s'%config_neutron_compute_sh, '%s'%remote_path, mode=777)
    put('%s'%config_file_sh, '%s'%remote_path, mode=777)
    rabbit_pwd=read_cfg_file("RABBITMQ",'password')
    local_ip=env.host_string.split('@')[1].split(':')[0]
    #compute_tun_ip=read_cfg_file("COMPUTE_TUN_IPS",'%s'%local_ip)
    compute_tun_ip='%s'%local_ip
 
    #with cd(remote_path),hide('stdout', 'stderr'):
    with cd(remote_path):
        run('%s/%s %s %s %s'%(remote_path,config_neutron_compute_sh,neutron_db_pwd,rabbit_pwd,compute_tun_ip))
        run('rm %s'%config_neutron_compute_sh)

@task
@roles('controller')
def check_network():
    with cd(remote_path),prefix('source admin-openrc.sh'):
	run('neutron agent-list')
 
@task
@roles('network')
def network():
    execute(create_networkdb)
    execute(init_neutrondb)
    execute(install_contollernode)
    execute(config_controllernode)
    execute(config_image)
    execute(check_image)
    execute(install_networknode)
    execute(config_networknode)
    execute(install_computenode)
    execute(config_computenode)
    execute(check_network)
      

