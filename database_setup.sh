#!/bin/bash

create_db="CREATE DATABASE IF NOT EXISTS jamjar"
mysql -uroot -proot -e "$create_db"
echo "created jamjar database"

create_user="GRANT ALL ON *.* TO 'jamjar'@'localhost' IDENTIFIED BY 'jamjar';"
mysql -uroot -proot -e "$create_user"
echo "User maadbox with password 'password' created"

