# WeatherAPI

This is an API that returns the weather for a particular city in a country. The service used to get the real data is [OpenWeatherMap](http://api.openweathermap.org)   

## Table of contents

#### 1. [ Description ](#desc)

#### 2. [ Stack ](#stack)

#### 3. [ Getting started ](#getting)

#### 4. [ Usage ](#usage)

#### 5. [ Solution ](#solution)

#### 6. [ Troubleshooting ](#troubleshooting)

#### 7. [ TODO ](#todo)


<a name="desc"></a>
### 1. Description

This API includes two endpoint: `health` & `weather`. The former is used to check the service is up and running whilst the latter is the endpoint that is going to provide the current weather for a particular city.


<a name="stack"></a>
### 2. Stack

- Flask
- Docker
- bash

<a name="getting"></a>
### 3. Getting started

The repository includes a `start` script that automates all the tasks needed to:
- Generate self-signed secrets to be used under https from local environment
- Build the docker image
- Start the docker container

There is also another `test` script that executes the commands for the coverage for the unit testing over the API

<a name="usage"></a>
### 4. Usage

#### Prerequisites

- Docker, since the script will execute everything from scratch
- export the following env vars:
  - `export WEATHER_ENDPOINT=http://api.openweathermap.org`
  - `export WEATHER_APP_ID=MY_API`
- execute `sh test.sh` to check the coverage and execute the unit tests. This is done through a different dockerfile: `Dockerfile._test` to implemtn the separation of concerns principle
- execute `sh start.sh`  to start the API in the local environment
- execute `curl -kv https://localhost:10443/weather/data\?city\=Bogota\&country\=co` to get the weather for the provided city.

<a name="solution"></a>
### 5. Solution
The proposed solution for this API was to take the Blueprint approach provided by Flask. The `weather` endpoint which is the core of the application, includes:
- The `WeatherAPIAdapter` which plays the role of fetching data from the provider. the idea behind this is to include scalability to the application. If the source of the data changes over time we would need to alter only this file or add other adapters like connection to DB for instance.
- The `WeatherService` which becomes the service called by the handler. Its main task is to validate the data that comes from the request. If the data is correct it invokes the `WeatherAPIAdapter` to fetch the data form the provider. It also raises Error/Exceptions if the input is wrong.
- The `WeatherMap` is a class that format the raw data from the provider to a friendly user response
- The handler, that starts the process on receiving the request and mapping the data that comes from the provider to the `WeatherAPI` format
- A set of custom Errors/Exceptions that are raised when something fails. The scenarios covered by the exceptions are check the env vars for `WEATHER_ENDPOINT` and `WEATHER_APP_ID` and if the request is missing either the country or the city.

<a name="troubleshooting"></a>
### 6. Troubleshooting
If either of the both automated scripts fails it is because the permissions need to be updated. The execution permissions get lost since the repo is brand new in the directory. To sort this out execute `chmod +x start.sh` & `chmod +x test.sh` and execute them.

<a name="todo"></a>
### 7. TODO
- Implement automated functional tests to check if the endpoint is up & running
- Cover more scenarios to the list of Errors/Exceptions like invalid inputs
- Deploy to Heroku through a GitHub actions pipeline
- Push the docker image to a registry (public or private)
- Include Auth0 authentication (user & password for instance) to generate/validate JWT token for consecutive calls