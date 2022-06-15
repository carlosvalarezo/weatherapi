import json

from flask import abort, Blueprint, jsonify, request
from http import HTTPStatus
from pymapper import Mapper
from datetime import datetime

import logging
import os
import requests


class WeatherError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


class EndpointNotSetError(WeatherError):
    def __init__(self, error, status_code):
        super().__init__(error, status_code)


class ApiKeyNotSetError(WeatherError):
    def __init__(self, error, status_code):
        super().__init__(error, status_code)


class CountryNotFoundException(WeatherError):
    def __init__(self, error, status_code):
        super().__init__(error, status_code)


class CityNotFoundException(WeatherError):
    def __init__(self, error, status_code):
        super().__init__(error, status_code)


class WeatherAPIAdapter:

    @staticmethod
    def _get_weather_url_endpoint():
        endpoint_env = os.environ.get('WEATHER_ENDPOINT', None)
        if endpoint_env is None:
            raise EndpointNotSetError("Please set the weather endpoint env var", HTTPStatus.NOT_FOUND)
        return endpoint_env

    @staticmethod
    def _get_app_id():
        weather_app_id = os.environ.get('WEATHER_APP_ID', None)
        if weather_app_id is None:
            raise ApiKeyNotSetError("Please set the weather api key env var", HTTPStatus.NOT_FOUND)
        return weather_app_id

    def get_weather_data(self, city, country):
        weather_service = self._get_weather_url_endpoint()
        weather_app_id = self._get_app_id()
        weather_url = f"{weather_service}/data/2.5/weather?q={city},{country}&appid={weather_app_id}"
        res = requests.get(weather_url)
        return res.json()


class WeatherService:
    @staticmethod
    def get_weather_data(city, country):
        if city is None:
            raise CityNotFoundException({
                'code': 'missing_city',
                'description': 'The city was not included in the request'
            }, 404)
        if country is None:
            raise CountryNotFoundException({
                'code': 'missing_country',
                'description': 'The country was not included in the request'
            }, 404)
        weather_adapter = WeatherAPIAdapter()
        return weather_adapter.get_weather_data(city=city, country=country)


class WeatherMap:
    KELVIN_FACTOR = 273.15

    def __init__(self, data) -> None:
        self.location_name = self._set_location(self, data)
        self.temperature = self._set_temperature(self, data)
        self.wind = self._set_wind(self, data)
        self.cloudiness = self._set_cloudiness(self, data)
        self.pressure = self._set_pressure(self, data)
        self.humidity = self._set_humidity(self, data)
        self.sunrise = self._set_sunrise(self, data)
        self.sunset = self._set_sunset(self, data)
        self.geo_coordinates = self._set_geo_coordinates(self, data)

    @staticmethod
    def _set_location(self, data: dict) -> str:
        country = data["sys"]["country"]
        city = data['name']
        return f'{city}, {str.upper(country)}'

    @staticmethod
    def _set_temperature(self, data: dict) -> str:
        return f'{int(data["main"]["temp"]) - self.KELVIN_FACTOR} C'

    @staticmethod
    def _set_wind(self, data: dict) -> str:
        return data["wind"]["speed"]

    @staticmethod
    def _set_cloudiness(self, data: dict) -> str:
        return data["weather"][0]["description"]

    @staticmethod
    def _set_pressure(self, data: dict) -> str:
        return data["main"]["pressure"]

    @staticmethod
    def _set_humidity(self, data: dict) -> str:
        return data["main"]["humidity"]

    @staticmethod
    def _set_sunrise(self, data: dict) -> str:
        value = data["sys"]["sunrise"]
        d = datetime.fromtimestamp(value)
        return f'{d.hour}:{d.minute}'

    @staticmethod
    def _set_sunset(self, data: dict) -> str:
        value = data["sys"]["sunset"]
        d = datetime.fromtimestamp(value)
        return f'{d.hour}:{d.minute}'

    @staticmethod
    def _set_geo_coordinates(self, data: dict) -> str:
        return f'{data["coord"]["lat"]}, {data["coord"]["lon"]}'


weather_endpoint = Blueprint('weather', __name__)


def _get_city(req):
    return req.args.get('city', None, type=str)


def _get_country(req):
    return req.args.get('country', None, type=str)


def _map_to_response(data):
    data_json = json.loads(data)
    weather_map = WeatherMap(data_json)
    mapper = Mapper({
        'location_name': '$source_1',
        'temperature': '$source_2',
        'wind': '$source_3',
        'cloudiness': '$source_4',
        'pressure': '$source_5',
        'humidity': '$source_6',
        'sunrise': '$source_7',
        'sunset': '$source_8',
        'geo_coordinates': '$source_9',
        'requested_time': '$source_10',
    })

    return mapper.map({
        'source_1': weather_map.location_name,
        'source_2': weather_map.temperature,
        'source_3': weather_map.wind,
        'source_4': weather_map.cloudiness,
        'source_5': weather_map.pressure,
        'source_6': weather_map.humidity,
        'source_7': weather_map.sunrise,
        'source_8': weather_map.sunset,
        'source_9': weather_map.geo_coordinates,
        'source_10': datetime.now(),
    })


@weather_endpoint.route('data', methods=['GET'])
def weather():
    try:
        city = _get_city(req=request)
        country = _get_country(req=request)
        weather_service = WeatherService()
        raw_data = weather_service.get_weather_data(city=city, country=country)
        return jsonify(_map_to_response(json.dumps(raw_data)))
    except (CountryNotFoundException, CityNotFoundException) as e:
        logging.error(e)
        abort(e)
