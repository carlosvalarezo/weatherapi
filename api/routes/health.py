from flask import Blueprint, jsonify

health_endpoint = Blueprint('api', __name__)


@health_endpoint.route('health')
def health():
    return jsonify({'status': 'up'})
