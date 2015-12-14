#!/usr/bin/env python
# encoding: utf-8
from fabric_env import *

neutron_db_pwd=read_cfg_file('NEUTRON','db_password')

@task
@roles('controller')
def install_dashboard():
    #with cd(remote_path),hide('stdout', 'stderr'):
    with cd(remote_path):
        run('apt-get install openstack-dashboard -y')

@task
@roles('controller')
def config_dashboard():
    config_file_sh="config_file.sh"
    config_dashboard_sh="config_dashboard.sh"

    put('%s'%config_dashboard_sh, '%s'%remote_path, mode=777)
    put('%s'%config_file_sh, '%s'%remote_path, mode=777)

    with cd(remote_path):
    #with cd(remote_path),hide('stdout', 'stderr'):
        run('%s/%s'%(remote_path,config_dashboard_sh))
        run('rm %s'%config_dashboard_sh)

@task
@roles('controller')
def restart_controller_services():
    with cd(remote_path):
         run('./restart_controller.sh')  
         run('rm os_exception.sh')
         run('rm cirros-0.3.4-x86_64-disk.img') 

@task
@roles('network')
def restart_network_services():
    with cd(remote_path):
         run('./restart_network.sh')
         run('rm os_exception.sh')  
 
@task
@roles('compute')
def remove_sh_files():
    with cd(remote_path):
         run('rm config_file.sh')
         run('rm os_exception.sh')   
 
@task
@roles('controller')
def dashboard():
    execute(install_dashboard)
    execute(config_dashboard)
    execute(restart_network_services)
    execute(restart_controller_services)
    execute(remove_sh_files)
      

