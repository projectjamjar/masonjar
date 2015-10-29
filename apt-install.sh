#!/bin/bash

apt-get update
apt-get install -y apache2 python-dev python-pip python-virtualenv libmysqlclient-dev zip 

a2enmod proxy_http
cp apache2.conf /etc/apache2/
service apache2 restart
