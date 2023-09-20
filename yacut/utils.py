from http import HTTPStatus
import random

from flask import abort
from sqlalchemy.exc import SQLAlchemyError

from . import db
from .constants import AVAILABLE_CHARS, ID_MAX_LENGTH
from .models import URLMap


def get_unique_short_id():
    while True:
        short_id = ''.join(
            [random.choice(AVAILABLE_CHARS) for _ in range(ID_MAX_LENGTH)]
        )
        try:
            if not URLMap.query.filter_by(short=short_id).first():
                return short_id
        except SQLAlchemyError:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR)


def save_to_db(object):
    try:
        db.session.add(object)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)
