#!/usr/bin/env python
# encoding: utf-8
from fabric_env import *

nova_db_pwd=read_cfg_file('NOVA','db_password')

@task
@roles('controller')
def install_contollernode():
    with cd(remote_path):
        run('apt-get install -y nova-api nova-cert nova-conductor nova-consoleauth \
  nova-novncproxy nova-scheduler python-novaclient')

@task
@roles('controller')
def config_controllernode():
    config_file_sh="config_file.sh"
    config_nova_controller_sh="config_nova_controller.sh"
    
    put('%s'%config_nova_controller_sh, '%s'%remote_path, mode=777)
    put('%s'%config_file_sh, '%s'%remote_path, mode=777)
    
    rabbit_pwd=read_cfg_file("RABBITMQ",'password')
    local_ip=env.host_string.split('@')[1].split(':')[0]

    with cd(remote_path),hide('stdout', 'stderr'):
        run('%s/%s %s %s %s'%(remote_path,config_nova_controller_sh,nova_db_pwd,rabbit_pwd,local_ip))
        run('rm %s'%config_nova_controller_sh)
        run('rm %s'%config_file_sh)

@task
@roles('compute')
@parallel
def install_computenode():
    #with cd(remote_path),hide('stdout', 'stderr'):
    with cd(remote_path):
	run('apt-get install nova-compute sysfsutils -y')

@task
@roles('controller')
def init_computedb():
    with cd(remote_path),prefix('source admin-openrc.sh'):
        run('openstack user create --password-prompt nova')
        run('openstack role add --project service --user nova admin')
        run('openstack service create --name nova \
             --description "OpenStack Compute service" compute')
        run('openstack endpoint create \
             --publicurl http://controller:8774/v2/%\(tenant_id\)s \
             --internalurl http://controller:8774/v2/%\(tenant_id\)s \
             --adminurl http://controller:8774/v2/%\(tenant_id\)s \
             --region RegionOne \
             compute')
     
@task
@roles('controller')
def create_computedb():
    db_ip="localhost"
    db_pwd=read_cfg_file('DATABASE','root_password')
    grant_privailege_sh="grant_privaileges.sh"      
    db_name="nova"
 
    with cd(remote_path):
         run('mysql -uroot -p%s -h%s -e "DROP DATABASE IF EXISTS %s;" '%(db_pwd,db_ip,db_name))
         run('mysql -uroot -p%s -h%s -e "CREATE DATABASE %s;" '%(db_pwd,db_ip,db_name))
    put('%s'%grant_privailege_sh, '%s'%remote_path, mode=777)
    with cd(remote_path):
        run('%s/%s %s %s %s %s'%(remote_path,grant_privailege_sh,db_pwd,db_ip,nova_db_pwd,db_name))
        run('rm %s/%s'%(remote_path,grant_privailege_sh))

@task
@roles('compute')
def config_computenode():
    config_file_sh="config_file.sh"
    config_nova_compute_sh="config_nova_compute.sh"
    os_exception="os_exception.sh"
    restart_compute_sh="restart_compute.sh"
 
    put('%s'%config_nova_compute_sh, '%s'%remote_path, mode=777)
    put('%s'%config_file_sh, '%s'%remote_path, mode=777)
    put('%s'%os_exception, '%s'%remote_path, mode=777)
    put('%s'%restart_compute_sh, '%s'%remote_path, mode=777)
    
    rabbit_pwd=read_cfg_file("RABBITMQ",'password')
    local_ip=env.host_string.split('@')[1].split(':')[0]
    vncserver_ip=read_cfg_file("CONTROLLER_NODE",'manage_ip') 
      
    #with cd(remote_path),hide('stdout', 'stderr'):
    with cd(remote_path):
        run('%s/%s %s %s %s %s'%(remote_path,config_nova_compute_sh,nova_db_pwd,rabbit_pwd,local_ip,vncserver_ip))
        run('rm %s'%config_nova_compute_sh)
        run('rm %s'%config_file_sh)
        

@task
@roles('controller')
def check_compute():
    with cd(remote_path),prefix('source admin-openrc.sh'):
	run('nova service-list')
        run('nova endpoints')
        #run('nova image-list')
 
@task
@roles('controller')
def compute():
    execute(create_computedb)
    execute(init_computedb)
    execute(install_contollernode)
    execute(config_controllernode)
    execute(install_computenode)
    execute(config_computenode)
    execute(check_compute)
      

