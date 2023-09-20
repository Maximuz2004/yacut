from http import HTTPStatus
import re

from flask import abort
from sqlalchemy.exc import SQLAlchemyError

from .constants import MAX_QUANTITY_DB_ITEMS, SHORT_PATTERN, URL_PATTERN
from .models import URLMap


def is_db_full():
    try:
        return URLMap.query.count() >= MAX_QUANTITY_DB_ITEMS
    except SQLAlchemyError:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)


def already_exist(short):
    try:
        return bool(URLMap.query.filter_by(short=short).first())
    except SQLAlchemyError:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)


def is_valid_url(url):
    if URL_PATTERN.match(url):
        return True
    else:
        return False


def is_correct_len(input_str, min_len, max_len):
    return min_len <= len(input_str) <= max_len


def is_correct_chars(input_string):
    return re.match(SHORT_PATTERN, input_string)
