# -*- coding:utf-8 -*-
import os
import sys,os,time
import socket, fcntl, struct
import ConfigParser

def get_pwd():
    pwd = sys.path[0]
    if os.path.isfile(pwd):
        pwd = os.path.dirname(pwd)
    return pwd

config_file_path = get_pwd()+"/config.ini"

def read_cfg_file(field, key):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read(config_file_path)
        result = cf.get(field, key)
    except Exception,e:
        import traceback
        traceback.print_stack()
        traceback.print_exc()
        sys.exit(1)
    return result

compute_number=read_cfg_file("COMPUTE","compute_number")
#print "compute_number=%s"%compute_number
compute=""
host_ip_name={}
for i in range(int(compute_number)):
    i=i+1
    ip=read_cfg_file("COMPUTE_NODE%s"%str(i),"manage_ip")
    name="compute%s"%str(i)
    #host_ip_name=
    compute=compute+ip+" "+name+"\n"

controller_ip=read_cfg_file("CONTROLLER_NODE","manage_ip")
network_ip=read_cfg_file("NETWORK_NODE","manage_ip")

controller_network="127.0.0.1 localhost\n%s controller\n%s network\n"%(controller_ip,network_ip)
ipv6="::1 localhost ip6-localhost ip6-loopback\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters"
etc_hosts=controller_network+compute+ipv6

file_object = open('hosts', 'w')
file_object.write(etc_hosts)
file_object.close()
