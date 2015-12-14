#!/usr/bin/env python
# encoding: utf-8
from fabric_env import *

glance_db_pwd=read_cfg_file('IMAGE','db_password')

@task
@roles('controller')
def install_glance():
    with cd(remote_path):
        run('apt-get install -y glance python-glanceclient')

@task
@roles('controller')
def init_imagedb():
    with cd(remote_path),prefix('source admin-openrc.sh'):
        run('openstack user create --password-prompt glance')
        run('openstack role add --project service --user glance admin')
        run('openstack service create --name glance \
             --description "OpenStack Image service" image')
        run('openstack endpoint create \
             --publicurl http://controller:9292 \
             --internalurl http://controller:9292 \
             --adminurl http://controller:9292 \
            --region RegionOne \
            image')
     
@task
@roles('controller')
def create_imagedb():
    db_ip="localhost"
    db_pwd=read_cfg_file('DATABASE','root_password')
    grant_privailege_sh="grant_privaileges.sh"      
    db_name="glance"
 
    with cd(remote_path):
         run('mysql -uroot -p%s -h%s -e "DROP DATABASE IF EXISTS %s;" '%(db_pwd,db_ip,db_name))
         run('mysql -uroot -p%s -h%s -e "CREATE DATABASE %s;" '%(db_pwd,db_ip,db_name))
    put('%s'%grant_privailege_sh, '%s'%remote_path, mode=777)
    with cd(remote_path):
        run('%s/%s %s %s %s %s'%(remote_path,grant_privailege_sh,db_pwd,db_ip,glance_db_pwd,db_name))
        run('rm %s/%s'%(remote_path,grant_privailege_sh))

@task
@roles('controller')
def config_glance():
    config_file_sh="config_file.sh"
    config_glance_sh="config_glance.sh"
    os_exception="os_exception.sh"    
    
    put('%s'%config_file_sh, '%s'%remote_path, mode=777)
    put('%s'%config_glance_sh, '%s'%remote_path, mode=777)
    put('%s'%os_exception, '%s'%remote_path, mode=777)
        
    glance_db_pwd=read_cfg_file("IMAGE",'db_password')
    with cd(remote_path):
        run('%s/%s %s'%(remote_path,config_glance_sh,glance_db_pwd))
        run('rm %s'%config_glance_sh)

@task
@roles('controller')
def image():
    execute(create_imagedb)
    execute(init_imagedb)
    execute(install_glance)
    execute(config_glance)
      

