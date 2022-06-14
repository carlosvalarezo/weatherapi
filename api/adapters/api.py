import os
import requests

from api.errors.api_key_not_set import ApiKeyNotSetError
from api.errors.endpoint_not_set import EndpointNotSetError
from http import HTTPStatus


class WeatherAPIAdapter:

    @staticmethod
    def _get_weather_url_endpoint():
        weather_endpoint = os.environ.get('WEATHER_ENDPOINT', None)
        if weather_endpoint is None:
            raise EndpointNotSetError("Please set the weather endpoint env var", HTTPStatus.NOT_FOUND)

    @staticmethod
    def _get_app_id():
        weather_app_id = os.environ.get('WEATHER_APP_ID', None)
        if weather_app_id is None:
            raise ApiKeyNotSetError("Please set the weather api key env var", HTTPStatus.NOT_FOUND)

    def get_weather_data(self, city, country):
        weather_endpoint = self._get_weather_url_endpoint()
        weather_app_id = self._get_app_id()
        weather_url = f"{weather_endpoint}/data/2.5/weather?q={country},{city}&appid={weather_app_id}"
        res = requests.get(weather_url)
        return res.json()
