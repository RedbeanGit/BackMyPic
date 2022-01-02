#!/usr/bin/env bash

if [ ${PWD##*/} == scripts ] ;
then
    cd ..
fi

. scripts/utils.sh

echop 'Installing python packages...'
python3 -m pip install -r requirements.txt
echop 'Python packages have been installed!'
echo