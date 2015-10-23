#!/bin/bash

if [ ! -d env ]; then
  virtualenv env
fi
echo "Virtualenv created"

source env/bin/activate
pip install -r requirements.txt
echo "Requirements installed"

create_user="GRANT ALL ON *.* TO 'jmajar'@'localhost' IDENTIFIED BY 'jamjar';"
mysql -uroot -proot -e "$create_user"
echo "User maadbox with password 'password' created"

create_db="CREATE DATABASE IF NOT EXISTS jamjar"
mysql -uroot -proot -e "$create_db"
echo "created jamjar database"
