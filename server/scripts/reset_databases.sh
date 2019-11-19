#!/bin/bash

source .env

mysql -u$APP_DB_USER -p$APP_DB_PASS -h$APP_DB_HOST -e "show databases" | grep -v Database | grep -v mysql| grep -v information_schema | grep -v test | grep -v OLD |gawk '{print "drop database " $1 ";select sleep(0.1); DROP USER IF EXISTS " $1 ";"}' | mysql -u$APP_DB_USER -p$APP_DB_PASS -h$APP_DB_HOST

./upgrade.sh