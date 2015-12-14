#!/usr/bin/env python
# encoding: utf-8
from config import *


@task
@roles('base_env')
def base_env():
    host_ip=env.host_string.split('@')[1].split(':')[0]
    with cd(remote_path):
        run('openssl rand -hex 10 > hex.tmp')
