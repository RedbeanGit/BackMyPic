#!/usr/bin/env bash

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

. scripts/utils.sh

echop 'Welcome to Picdo setup.'
echop 'This script will let you define variables for your local environment.'
echop 'The proposals in brackets are the default values. Leave blank to use them.'

echo
read -p 'Database name (picdo): ' db_name
read -p 'Database host (db): ' db_host
read -p 'Database port (5432): ' db_port
read -p 'Database user (postgres): ' db_user
read -sp 'Database password (auto generated): ' db_password && echo
read -sp 'Django secret key (auto generated):' secret_key && echo
echo

if [ -z "$db_name" ]
then
    db_name=picdo
fi

if [ -z "$db_host" ]
then
    db_host=db
fi

if [ -z "$db_port" ]
then
    db_port=5432
fi

if [ -z "$db_user" ]
then
    db_user=postgres
fi

if [ -z "$db_password" ]
then
    db_password=$(openssl rand -base64 48)
fi

if [ -z "$secret_key" ]
then
    secret_key=$(openssl rand -base64 48)
fi

version=$(cat VERSION)

echo "PICDO_VERSION='$version'" > .env
echo "PICDO_SECRET_KEY='$secret_key'" >> .env
echo "PICDO_ENVIRONMENT='DEVELOPMENT'" >> .env
echo "PICDO_DB_NAME='$db_name'" >> .env
echo "PICDO_DB_HOST='$db_host'" >> .env
echo "PICDO_DB_PORT='$db_port'" >> .env
echo "PICDO_DB_USER='$db_user'" >> .env
echo "PICDO_DB_PASSWORD='$db_password'" >> .env

echop 'Environment variables have been defined!'