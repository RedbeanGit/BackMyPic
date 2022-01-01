#!/usr/bin/env bash

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

set -a
. .env
set +a

docker-compose up --build