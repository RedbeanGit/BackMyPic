#!/usr/bin/env sh

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

export picdo_version=$(cat VERSION)
export picdo_secret_key=$(jq '."secret_key"' secrets.json)
export picdo_environment='DEVELOPMENT'
export picdo_db_name='picdo'
export picdo_db_host='db'
export picdo_db_port='5432'
export picdo_db_user='postgres'
export picdo_db_password=$(jq '."postgres_key"' secrets.json)

docker build -t redbeandock/picdo:$picdo_version .
docker push redbeandock/picdo:$picdo_version
docker-compose up