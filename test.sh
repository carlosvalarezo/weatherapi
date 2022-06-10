#!/bin/bash

docker build . -t carlosvalarezo/weather-api-tests -f Dockerfile._test
docker run --rm --name weather-api-tests -v $PWD/api:/api carlosvalarezo/weather-api-tests
