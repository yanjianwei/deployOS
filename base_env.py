#!/usr/bin/env python
# encoding: utf-8
from fabric_env import *

@task
@roles('controller')
def install_controller_ntp():
    with cd(remote_path):
        run('apt-get install -y ntp')
        run("sed -i 's/ntp.ubuntu.com/controller iburst/g' /etc/ntp.conf && sed -i 's/nopeer noquery/ /g' /etc/ntp.conf")
        run('service ntp restart')
        run('ntpq -c peers')
        run('ntpq -c assoc')

@task
@roles('network','compute')
@parallel
def install_networkcompute_ntp():
    with cd(remote_path):
        run('apt-get install -y ntp')
        run('echo "server controller iburst" > /etc/ntp.conf')
        run('service ntp restart')
        run('ntpq -c peers')
        run('ntpq -c assoc')

@task
@roles('controller')
def create_randhex():
    with cd(remote_path),hide('stdout', 'stderr'):
        run('openssl rand -hex 10 > hex.tmp')

@task
@parallel
def update_ubuntu_repository():
    with cd(remote_path):
    #with cd(remote_path):
        run('apt-get install ubuntu-cloud-keyring')
        run('echo "deb http://ubuntu-cloud.archive.canonical.com/ubuntu" \
  "trusty-updates/kilo main" > /etc/apt/sources.list.d/cloudarchive-kilo.list')
        run('apt-get update ')
        run('apt-get dist-upgrade -y')

@task
@roles('controller')
def install_database():
    controller_manage_ip=env.host_string.split('@')[1].split(':')[0]
    db_cfg="mysql_cfg.sh"
    db_pwd=read_cfg_file('DATABASE','root_password')   
    install_database_sh="install_database.sh"
    restart_controller_sh="restart_controller.sh"
    demo_net_sh="create_demo_net.sh"
    ext_net_sh="create_ext_net.sh" 
 
    put('%s'%install_database_sh, '%s'%remote_path, mode=777)
    put('%s'%db_cfg, '%s'%remote_path, mode=777)
    put('%s'%restart_controller_sh, '%s'%remote_path, mode=777)
    put('%s'%demo_net_sh, '%s'%remote_path, mode=777)
    put('%s'%ext_net_sh, '%s'%remote_path, mode=777)
  
    with cd(remote_path):
        run('%s/%s %s'%(remote_path,install_database_sh,db_pwd))
        run('%s/%s %s'%(remote_path,db_cfg,controller_manage_ip))
        run('rm %s/%s'%(remote_path,db_cfg))
        run('service mysql restart')
        run('rm %s'%install_database_sh)

@task
@roles('controller')
def install_rabbitmq():
    controller_manage_ip=env.host_string.split('@')[1].split(':')[0]
    rabbit_pwd=read_cfg_file('RABBITMQ','password')

    with cd(remote_path):
        run('apt-get install -y rabbitmq-server')
        run('rabbitmqctl add_user openstack %s'%rabbit_pwd)
        run('rabbitmqctl set_permissions openstack ".*" ".*" ".*"') 
        
@task
@roles('controller')
def base_env():
    execute(install_controller_ntp)  
    execute(install_networkcompute_ntp)
    execute(update_ubuntu_repository)
    execute(install_database)
    execute(install_rabbitmq)
      

