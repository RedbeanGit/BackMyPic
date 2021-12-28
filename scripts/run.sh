#!/usr/bin/env bash

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

set -a
. .env
set +a

docker build -t "redbeandock/picdo:${PICDO_VERSION}" .
docker push "redbeandock/picdo:${PICDO_VERSION}"
docker-compose up