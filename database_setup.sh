#!/bin/bash

create_db="CREATE DATABASE IF NOT EXISTS jamjar"
mysql -uroot -proot -e "$create_db"
echo "created jamjar database"

create_user="GRANT ALL ON *.* TO 'jamjar'@'localhost' IDENTIFIED BY 'jamjar';"
mysql -uroot -proot -e "$create_user"
echo "User maadbox with password 'password' created"

create_db="CREATE DATABASE IF NOT EXISTS dejavu"
mysql -uroot -proot -e "$create_db"
echo "created dejavu database"

create_db="CREATE DATABASE IF NOT EXISTS dejavu_test"
mysql -uroot -proot -e "$create_db"
echo "created dejavu_test database"

create_user="GRANT ALL ON *.* TO 'jamjar'@'localhost' IDENTIFIED BY 'jamjar';"
mysql -uroot -proot -e "$create_user"
echo "User jamjar with password 'jamjar' created"


