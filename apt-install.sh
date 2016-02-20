#!/bin/bash

if [ "$(id -u)" != "0" ]; then
    echo "Please run this script as sudo."
    exit 1
fi

apt-get update
apt-get install -y apache2 python-dev python-pip python-virtualenv libmysqlclient-dev zip
apt-get install -y python-numpy python-scipy python-matplotlib libportaudio-dev python-PyAudio python-MySQLdb libav-tools
apt-get install -y pkg-config libblas-dev liblapack-dev libatlas-base-dev gfortran libpng-dev libfreetype6-dev imagemagick
apt-get install -y portaudio19-dev

# Install autoenv
pip install virtualenv autoenv
virtualenv env
echo "source `which activate.sh`" >> ~/.bashrc

a2enmod proxy_http
cp apache2.conf /etc/apache2/
service apache2 restart

# Install redis
wget -O /tmp/redis-3.0.6.tar.gz http://download.redis.io/releases/redis-3.0.6.tar.gz
tar -xvf /tmp/redis-3.0.6.tar.gz -C /tmp/
make -C /tmp/redis-3.0.6/
make -C /tmp/redis-3.0.6/ install
