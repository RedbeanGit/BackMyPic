#!/usr/bin/env sh

if [ "${PWD##*/}" = "scripts" ] ;
then
    cd ..
fi

secret_key=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
postgres_key=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
echo '{}' | jq ".\"secret_key\" = \"${secret_key}\" | .\"postgres_key\" = \"${postgres_key}\"" > secrets.json