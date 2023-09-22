from collections import namedtuple
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

GET_URL_ROUTE = '/api/id/<string:short_id>/'
CREATE_ID_ROUTE = '/api/id/'
NO_DATA_MESSAGE = 'Отсутствует тело запроса'
NO_URL_IN_REQUEST_MESSAGE = '\"url\" является обязательным полем!'
NO_SHORT_FOUND_MESSAGE = 'Указанный id не найден'
MODEL_FIELDS = namedtuple(
    'Fields',
    ['id', 'original', 'short', 'timestamp']
)
REQUEST_FIELDS = MODEL_FIELDS(None, 'url', 'custom_id', None)


@app.route(CREATE_ID_ROUTE, methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(NO_DATA_MESSAGE)
    original = data.get(REQUEST_FIELDS.original)
    if not original:
        raise InvalidAPIUsage(NO_URL_IN_REQUEST_MESSAGE)
    short = data.get(REQUEST_FIELDS.short)
    try:
        url_map = URLMap.create(original, short)
    except ValueError as error:
        raise InvalidAPIUsage(error.args[0])
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route(GET_URL_ROUTE, methods=['GET'])
def get_url(short_id):
    url_map = URLMap.get_url_map(short_id)
    if not url_map:
        raise InvalidAPIUsage(NO_SHORT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})
