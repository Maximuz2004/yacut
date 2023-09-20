from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import (GET_URL_ROUTE, CREATE_ID_ROUTE, NO_DATA_MESSAGE, NO_URL_IN_REQUEST_MESSAGE,
                        NO_SHORT_FOUND_MESSAGE, REQUEST_FIELDS)
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id, save_to_db
from .validators import validate_original, validate_short


@app.route(CREATE_ID_ROUTE, methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(NO_DATA_MESSAGE)
    original = data.get(REQUEST_FIELDS.original)
    if original:
        validate_original(original)
    else:
        raise InvalidAPIUsage(NO_URL_IN_REQUEST_MESSAGE)
    short = data.get(REQUEST_FIELDS.short)
    if short:
        validate_short(short)
    else:
        short = get_unique_short_id()
    url_map = URLMap()
    url_map.from_dict({'original': original, 'short': short})
    save_to_db(url_map)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route(GET_URL_ROUTE, methods=['GET'])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage(NO_SHORT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})
