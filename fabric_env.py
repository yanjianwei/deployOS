#!/usr/bin/env python
# encoding: utf-8

from fabric.api import *
import sys 
sys.path.insert(0, './common')
from tools import *

env.hosts = [ 
    'root@%s:22'%read_cfg_file('CONTROLLER_NODE','manage_ip'),
    'root@%s:22'%read_cfg_file('NETWORK_NODE','manage_ip'),
    'root@%s:22'%read_cfg_file('COMPUTE_NODE1','manage_ip'),
    'root@%s:22'%read_cfg_file('COMPUTE_NODE2','manage_ip'),
]

#for compute_node in range(len(read_cfg_file('COMPUTE_NODE','manage_ip').split(','))):
 #   env.hosts.append(compute_node)

env.passwords = {
    env.hosts[0]: '%s'%read_cfg_file('CONTROLLER_NODE','root_password'),
    env.hosts[1]: '%s'%read_cfg_file('NETWORK_NODE','root_password'),
    env.hosts[2]: '%s'%read_cfg_file('COMPUTE_NODE1','root_password'),
    env.hosts[3]: '%s'%read_cfg_file('COMPUTE_NODE2','root_password'),
}

env.roledefs = {
    'controller' : [env.hosts[0]],
    'network' : [env.hosts[1]],
    'compute' : [env.hosts[2],env.hosts[3]],
    #'compute' : [env.hosts[2]],
}

remote_path='%s'%read_cfg_file('PATH','remote_dir')
local_path='%s'%read_cfg_file('PATH','local_dir')
