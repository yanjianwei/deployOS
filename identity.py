#!/usr/bin/env python
# encoding: utf-8
from fabric_env import *

keystone_db_pwd=read_cfg_file('KEYSTONE','db_password')
admin_token=read_cfg_file('KEYSTONE','admin_token')

@task
@roles('controller')
def install_keystone():
    with cd(remote_path):
        run('echo "manual" > /etc/init/keystone.override')
        run('apt-get install -y keystone python-openstackclient apache2 libapache2-mod-wsgi memcached python-memcache')   

@task
@roles('controller')
def config_keystone():
    keystone_cfg="/etc/keystone/keystone.conf"
    config_file_sh="config_file.sh"
    config_keystone_sh="config_keystone.sh"
    with cd(remote_path):
        run('echo "manual" > /etc/init/keystone.override')
        run('apt-get install -y keystone python-openstackclient apache2 libapache2-mod-wsgi memcached python-memcache')   

    put('%s'%config_file_sh, '%s'%remote_path, mode=777)
    put('%s'%config_keystone_sh, '%s'%remote_path, mode=777)
    with cd(remote_path),hide('stdout', 'stderr'):
        run('%s/%s %s %s %s'%(remote_path,config_keystone_sh,keystone_cfg,keystone_db_pwd,admin_token))
        run('rm %s'%config_keystone_sh)

@task
@roles('controller')
def init_keystonedb():
    with cd(remote_path),prefix('export OS_TOKEN=%s && export OS_URL=http://controller:35357/v2.0'%admin_token):
        run('openstack service create --name keystone --description "OpenStack Identity" identity')
        run('openstack endpoint create \
            --publicurl http://controller:5000/v2.0 \
            --internalurl http://controller:5000/v2.0 \
            --adminurl http://controller:35357/v2.0 \
            --region RegionOne \
           identity')
        run('openstack project create --description "Admin Project" admin')
        run('openstack user create --password-prompt admin')
        run('openstack role create admin')
        run('openstack role add --project admin --user admin admin')
        run('openstack project create --description "Service Project" service')
        run('openstack project create --description "Demo Project" demo')
        run('openstack user create --password-prompt demo')
        run('openstack role create user')
        run('openstack role add --project demo --user demo user')
    with cd(remote_path):
        run('openstack --os-auth-url http://controller:35357 \
            --os-project-name admin --os-username admin --os-auth-type password token issue ')     
     
@task
@roles('controller')
def create_database():
    db_ip="localhost"
    db_pwd=read_cfg_file('DATABASE','root_password')
    grant_privailege_sh="grant_privaileges.sh"      
    db_name="keystone"
    
    with cd(remote_path):
         run('mysql -uroot -p%s -h%s -e "DROP DATABASE IF EXISTS %s;" '%(db_pwd,db_ip,db_name))
         run('mysql -uroot -p%s -h%s -e "CREATE DATABASE %s;" '%(db_pwd,db_ip,db_name))
    put('%s'%grant_privailege_sh, '%s'%remote_path, mode=777)
    with cd(remote_path):
        run('%s/%s %s %s %s %s'%(remote_path,grant_privailege_sh,db_pwd,db_ip,keystone_db_pwd,db_name))
        run('rm %s/%s'%(remote_path,grant_privailege_sh))

@task
@roles('controller')
def upload_openrc():
    admin_openrc="admin-openrc.sh"
    demo_openrc="demo-openrc.sh"

    put('%s'%admin_openrc, '%s'%remote_path, mode=777)
    put('%s'%demo_openrc, '%s'%remote_path, mode=777)
       
@task
@roles('controller')
def identity():
    execute(create_database)
    execute(install_keystone)
    execute(config_keystone)
    execute(init_keystonedb)
    execute(upload_openrc)

