#!/bin/bash
cp /etc/mysql/my.cnf /etc/mysql/my.cnf.bak`date +%Y-%m-%d-%H:%M`

sed -i "/^bind-address/s/127.0.0.1/$1\ndefault-storage-engine = innodb\ninnodb_file_per_table\ncollation-server = utf8_general_ci\ninit-connect = \'SET NAMES utf8\'\ncharacter-set-server = utf8/g" /etc/mysql/my.cnf
