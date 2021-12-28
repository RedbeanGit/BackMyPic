#!/usr/bin/env bash

echo 'Cleaning docker from Picdo containers and images...'

# deleting picdo containers
for name in picdo_picdo_1 picdo_db_1
do
    running_container=$(docker ps -f "name=$name" | tail -n +2)
    if [ ! -z "$running_container" ]
    then
        docker stop "$name"
    fi

    container=$(docker ps -a -f "name=$name" | tail -n +2)
    if [ ! -z "$container" ]
    then
        docker rm "$name"
    fi
done

# deleting picdo images
image=$(docker images -f "reference=redbeandock/picdo:*" -q)
if [ ! -z "$image" ]
then
    docker rmi "$image"
fi 

echo 'Done'