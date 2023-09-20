from http import HTTPStatus

from flask import jsonify, request

from . import app
from .constants import (DB_FULL_MESSAGE, ID_MAX_LENGTH, INVALID_CUSTOM_ID,
                        INVALID_ORIGINAL_LINK_MESSAGE, MIN_LENGTH,
                        NO_DATA_MESSAGE, NO_URL_IN_REQUEST_MESSAGE,
                        NO_SHORT_FOUND_MESSAGE, REQUEST_FIELDS,
                        SHORT_LINK_EXIST_MESSAGE_API)
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id, save_to_db
from .validators import (already_exist, is_correct_chars, is_correct_len,
                        is_db_full, is_valid_url, validate_short)


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(NO_DATA_MESSAGE)
    original = data.get(REQUEST_FIELDS.original)
    if original is None:
        raise InvalidAPIUsage(NO_URL_IN_REQUEST_MESSAGE)
    elif not is_valid_url(original):
        raise InvalidAPIUsage(INVALID_ORIGINAL_LINK_MESSAGE)
    short = data.get(REQUEST_FIELDS.short)
    if short:
        validate_short(short)
    else:
        short = get_unique_short_id()
    url_map = URLMap()
    url_map.from_dict({'original': original, 'short': short})
    save_to_db(url_map)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise InvalidAPIUsage(NO_SHORT_FOUND_MESSAGE, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original})
