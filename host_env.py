#!/usr/bin/env python
# encoding: utf-8
from fabric_env import *

@task
def create_etc_hosts():
    with lcd(local_path):
        local('python hosts.py') 

@task
@parallel
def config_hosts():
    etc_hosts="hosts"    
    source_list="sources.list"
       
    put('%s'%etc_hosts, '%s'%remote_path, mode=644)
    put('%s'%source_list, '%s'%remote_path, mode=644)
  
    with cd(remote_path):
        run('cp /etc/hosts /etc/hosts.bak')
        run('mv hosts /etc/')
        run('chmod 644 /etc/hosts')
        run('cp /etc/apt/sources.list /etc/apt/sources.list.bak')
        run('mv sources.list /etc/apt/')
        run('chmod 644 /etc/apt/sources.list')
        run('apt-get update')    

@task
@roles('controller')
def rename_controller_host():
    with cd(remote_path):
        run('echo "controller" >/etc/hostname')
        run('service hostname restart')

@task
@roles('network')
def rename_network_host():
    with cd(remote_path):
        run('echo "network" >/etc/hostname')
        run('service hostname restart')

#@task
#@roles('compute')
#def rename_compute_host():
#    with cd(remote_path):
         
        
@task
@roles('controller')
def host_env():
    create_etc_hosts()
    execute(config_hosts) 
    execute(rename_controller_host) 
    execute(rename_network_host) 
