from http import HTTPStatus
import re


from flask import abort
from sqlalchemy.exc import SQLAlchemyError

from .constants import (DB_FULL_MESSAGE, ID_MAX_LENGTH, INVALID_CUSTOM_ID,
                        INVALID_ORIGINAL_LINK_MESSAGE, MAX_QUANTITY_DB_ITEMS,
                        MIN_LENGTH, SHORT_LINK_EXIST_MESSAGE_API,
                        SERVER_ISSUE_ERROR, SHORT_PATTERN, URL_PATTERN)
from .error_handlers import InvalidAPIUsage
from .models import URLMap


ERROR_MESSAGES = {
    'invalid_length': INVALID_CUSTOM_ID,
    'invalid_chars': INVALID_CUSTOM_ID,
    'invalid_original': INVALID_ORIGINAL_LINK_MESSAGE,
    'short_link_exist': SHORT_LINK_EXIST_MESSAGE_API,
    'db_full': DB_FULL_MESSAGE,

}


def is_db_full(useless, error_type=None):
    try:
        return not URLMap.query.count() >= MAX_QUANTITY_DB_ITEMS
    except SQLAlchemyError:
        if error_type == 'api':
            raise InvalidAPIUsage(
                SERVER_ISSUE_ERROR,
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
        else:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)


def already_exist(short, error_type=None):
    try:
        return not bool(URLMap.query.filter_by(short=short).first())
    except SQLAlchemyError:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)


def is_valid_url(url, error_type=None):
    if URL_PATTERN.match(url):
        return True
    else:
        return False


def is_correct_len(input_str, error_type=None):
    return MIN_LENGTH <= len(input_str) <= ID_MAX_LENGTH


def is_correct_chars(input_string, error_type=None):
    return re.match(SHORT_PATTERN, input_string)


SHORT_VALIDATORS = [
    (is_correct_len, 'invalid_length'),
    (is_correct_chars, 'invalid_chars'),
    (already_exist, 'short_link_exist'),
    (is_db_full, 'db_full')
]
ORIGINAL_VALIDATORS = [
    (is_valid_url, 'invalid_original'),
]


def validate_short(short):
    for validator, error_key in SHORT_VALIDATORS:
        if not validator(short):
            raise InvalidAPIUsage(
                ERROR_MESSAGES.get(error_key).format(short=short)
            )


def validate_original(original):
    for validator, error_key in ORIGINAL_VALIDATORS:
        if not validator(original, error_type='api'):
            raise InvalidAPIUsage(ERROR_MESSAGES.get(error_key))
