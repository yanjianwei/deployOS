#!/bin/bash
db_pwd=$1
export DEBIAN_FRONTEND=noninteractive
debconf-set-selections <<< "mariadb-server-5.5 mysql-server/root_password password $db_pwd" 
debconf-set-selections <<< "mariadb-server-5.5 mysql-server/root_password_again password $db_pwd"
apt-get install mariadb-server python-mysqldb -y
