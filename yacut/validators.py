from http import HTTPStatus
import re


from flask import abort
from sqlalchemy.exc import SQLAlchemyError

from .constants import (DB_FULL_MESSAGE, ID_MAX_LENGTH, INVALID_CUSTOM_ID,
                        MAX_QUANTITY_DB_ITEMS, MIN_LENGTH, SHORT_LINK_EXIST_MESSAGE_API,
                        SHORT_PATTERN, URL_PATTERN)
from .error_handlers import InvalidAPIUsage
from .models import URLMap


ERROR_MESSAGES = {
    'invalid_length': INVALID_CUSTOM_ID,
    'invalid_chars': INVALID_CUSTOM_ID,
    'short_link_exist': SHORT_LINK_EXIST_MESSAGE_API,
    'db_full': DB_FULL_MESSAGE,

}


def is_db_full(useless):
    try:
        return not URLMap.query.count() >= MAX_QUANTITY_DB_ITEMS
    except SQLAlchemyError:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)


def already_exist(short):
    try:
        return not bool(URLMap.query.filter_by(short=short).first())
    except SQLAlchemyError:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)


def is_valid_url(url):
    if URL_PATTERN.match(url):
        return True
    else:
        return False


def is_correct_len(input_str):
    return MIN_LENGTH <= len(input_str) <= ID_MAX_LENGTH


def is_correct_chars(input_string):
    return re.match(SHORT_PATTERN, input_string)


SHORT_VALIDATORS = [
    (is_correct_len, 'invalid_length'),
    (is_correct_chars, 'invalid_chars'),
    (already_exist, 'short_link_exist'),
    (is_db_full, 'db_full')
]


def validate_short(short):
    for validator, error_key in SHORT_VALIDATORS:
        if not validator(short):
            raise InvalidAPIUsage(ERROR_MESSAGES.get(error_key).format(short=short))