#!/usr/bin/env bash

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

. scripts/utils.sh

set -a
. .env
set +a

export PICDO_DB_HOST='localhost'

if [ ! "$(docker ps -a | grep picdo_db_2)" ]; then
    echop 'Creating postgresql container...'
    
    docker run \
    -d \
    -h "$PICDO_DB_HOST" \
    --name picdo_db_2 \
    -e POSTGRES_DB="$PICDO_DB_NAME" \
    -e POSTGRES_USER="$PICDO_DB_USER" \
    -e POSTGRES_PASSWORD="$PICDO_DB_PASSWORD" \
    -p "${PICDO_DB_PORT}:5432" \
    -v "${PWD}/scripts/docker:/docker-entrypoint-initdb.d" \
    postgres:14-alpine

    sleep 5
    
    echop 'Done'
elif [ ! "$(docker ps | grep picdo_db_2)" ]; then
    echop 'Starting postgresql...'
    docker start picdo_db_2
    echop 'Done'
fi

echop 'Populating database...'
python3 src/manage.py migrate
echop 'Done'

echop 'Running Picdo...'
python3 src/manage.py runserver 0.0.0.0:8000
echop 'Stopped'