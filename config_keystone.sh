#!/bin/bash

pwd_dir=$(cd "$(dirname "$0")"; pwd)
. $pwd_dir/config_file.sh
. $pwd_dir/os_exception.sh

KEYSTONE_CONF=$1
KEYSTONE_DB_PASSWORD=$2
ADMIN_TOKEN=$3

cp $KEYSTONE_CONF $KEYSTONE_CONF'.bak'`date +%Y-%m-%d-%H:%M`

iniset $KEYSTONE_CONF DEFAULT admin_token $ADMIN_TOKEN
iniset $KEYSTONE_CONF DEFAULT verbose  True 
iniset $KEYSTONE_CONF database connection mysql://keystone:$KEYSTONE_DB_PASSWORD@controller/keystone
iniuncomment  $KEYSTONE_CONF memcache servers
iniuncomment  $KEYSTONE_CONF token provider
iniset $KEYSTONE_CONF token driver keystone.token.persistence.backends.memcache.Token 
iniuncomment  $KEYSTONE_CONF revoke driver

su -s /bin/sh -c "keystone-manage db_sync" keystone

echo "ServerName controller" >> /etc/apache2/apache2.conf 

cat << EOF > /etc/apache2/sites-available/wsgi-keystone.conf 
Listen 5000
Listen 35357

<VirtualHost *:5000>
    WSGIDaemonProcess keystone-public processes=5 threads=1 user=keystone display-name=%{GROUP}
    WSGIProcessGroup keystone-public
    WSGIScriptAlias / /var/www/cgi-bin/keystone/main
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
    <IfVersion >= 2.4>
      ErrorLogFormat "%{cu}t %M"
    </IfVersion>
    LogLevel info
    ErrorLog /var/log/apache2/keystone-error.log
    CustomLog /var/log/apache2/keystone-access.log combined
</VirtualHost>

<VirtualHost *:35357>
    WSGIDaemonProcess keystone-admin processes=5 threads=1 user=keystone display-name=%{GROUP}
    WSGIProcessGroup keystone-admin
    WSGIScriptAlias / /var/www/cgi-bin/keystone/admin
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
    <IfVersion >= 2.4>
      ErrorLogFormat "%{cu}t %M"
    </IfVersion>
    LogLevel info
    ErrorLog /var/log/apache2/keystone-error.log
    CustomLog /var/log/apache2/keystone-access.log combined
</VirtualHost>
EOF

ln -s /etc/apache2/sites-available/wsgi-keystone.conf /etc/apache2/sites-enabled
mkdir -p /var/www/cgi-bin/keystone
curl http://git.openstack.org/cgit/openstack/keystone/plain/httpd/keystone.py?h=stable/kilo \
  | tee /var/www/cgi-bin/keystone/main /var/www/cgi-bin/keystone/admin
chown -R keystone:keystone /var/www/cgi-bin/keystone

chmod 755 /var/www/cgi-bin/keystone/*
rm -f /var/lib/keystone/keystone.db

service apache2 restart
