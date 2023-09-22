from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import (
    GET_URL_ROUTE, CREATE_ID_ROUTE, NO_DATA_MESSAGE,
    NO_URL_IN_REQUEST_MESSAGE, NO_SHORT_FOUND_MESSAGE,
    REQUEST_FIELDS
)
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route(CREATE_ID_ROUTE, methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(NO_DATA_MESSAGE)
    original = data.get(REQUEST_FIELDS.original)
    if not original:
        raise InvalidAPIUsage(NO_URL_IN_REQUEST_MESSAGE)
    short = data.get(REQUEST_FIELDS.short)
    url_map = URLMap.create_url_map(original, short)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route(GET_URL_ROUTE, methods=['GET'])
def get_url(short_id):
    url_map = URLMap.get_original_link(short_id)
    if not url_map:
        raise InvalidAPIUsage(NO_SHORT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})
