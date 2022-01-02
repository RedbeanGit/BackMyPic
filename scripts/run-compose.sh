#!/usr/bin/env bash

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

. scripts/utils.sh

set -a
. .env
set +a

echop 'Running docker-compose...'
docker-compose up --build
echop 'Stopped'