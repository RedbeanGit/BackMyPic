#!/usr/bin/env sh

containersId=$(docker ps -a | tail -n +2 | tr -s ' ' | cut -d' ' -f1)
for containerId in $containersId
do
    docker rm $containerId
done

imagesId=$(docker images | tail -n +2 | tr -s ' ' | cut -d' ' -f3)
for imageId in $imagesId
do
    docker rmi $imageId
done