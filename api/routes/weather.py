from flask import Blueprint, jsonify, request
from http import HTTPStatus

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
        weather_adapter = WeatherAPIAdapter()
        return weather_adapter.get_weather_data(city=city, country=country)


class ArgumentValidation:
    @staticmethod
    def check_valid_arguments(params):
        city = params.args.get('city', '', type=str)
        if city is None:
            raise CityNotFoundException({
                'code': 'missing_city',
                'description': 'The city was not included in the request'
            }, 404)
        country = params.args.get('country', '', type=str)
        if country is None:
            raise CountryNotFoundException({
                'code': 'missing_country',
                'description': 'The country was not included in the request'
            }, 404)
        return True


weather_endpoint = Blueprint('weather', __name__)


@weather_endpoint.route('data', methods=['GET'])
def weather():
    # ArgumentValidation.check_valid_arguments(request)
    city = request.args.get('city', None, type=str)
    country = request.args.get('country', None, type=str)
    weather_service = WeatherService()
    data = weather_service.get_weather_data(city=city, country=country)
    return jsonify(data)
