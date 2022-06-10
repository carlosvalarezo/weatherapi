#!/bin/bash

mkdir -p $PWD/api/certs
openssl req -x509 -out $PWD/api/certs/localhost.crt \
        -keyout $PWD/api/certs/localhost.key \
        -newkey rsa:2048 \
        -nodes -sha256 \
        -subj '/CN=localhost' -extensions EXT \
        -config $PWD/cert_config.cf
cp $PWD/api/certs/* $PWD/api/certs/
docker build . -t carlosvalarezo/weather-api
docker run -itp 10443:443 --rm --name weather-api \
       -v $PWD/api:/api carlosvalarezo/weather-api
