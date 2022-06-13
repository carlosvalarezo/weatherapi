import os
import requests

from api.errors.endpoint_not_found import EndpointNotSetError
from http import HTTPStatus


class WeatherAdapter:

    @staticmethod
    def _get_weather_url_endpoint():
        weather_endpoint = os.environ.get('WEATHER_ENDPOINT', None)
        if weather_endpoint is None:
            raise EndpointNotSetError("Please set the weather endpoint env var", HTTPStatus.NOT_FOUND)

    def get_weather_data(self):
        url = self._get_weather_url_endpoint()
        r = requests.get(url)
        return r.json()
