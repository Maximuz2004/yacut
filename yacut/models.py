from datetime import datetime
import random

from flask import url_for

from . import db
from .constants import (
    ATTEMPTS_COUNT, AVAILABLE_CHARS, ID_MAX_LENGTH, INVALID_CUSTOM_ID,
    INVALID_ORIGINAL_LINK_LENGTH, REDIRECT_VIEW, SHORT_ID_NOT_FOUND_MESSAGE,
    SHORT_LINK_EXIST_MESSAGE_API, URL_MAX_LENGTH
)
from .error_handlers import InvalidAPIUsage


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(URL_MAX_LENGTH),
        nullable=False,
        index=True,
    )
    short = db.Column(
        db.String(ID_MAX_LENGTH),
        nullable=False,
        index=True,
        unique=True
    )
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_VIEW,
                custom_id=self.short,
                _external=True
            )
        )

    @classmethod
    def create_url_map(cls, original, short=None):
        if short is None or short == '':
            short = URLMap.get_unique_short_id()
        cls.validate_api(original, short)
        instance = cls(original=original, short=short)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def validate_api(cls, original, short):
        short_length = len(short)
        original_length = len(original)
        if short_length > ID_MAX_LENGTH:
            raise InvalidAPIUsage(INVALID_CUSTOM_ID)
        if original_length > URL_MAX_LENGTH:
            raise InvalidAPIUsage(
                INVALID_ORIGINAL_LINK_LENGTH.format(
                    max_length=URL_MAX_LENGTH,
                    current_length=original_length
                )
            )
        incorrect_chars = set(short).difference(set(AVAILABLE_CHARS))
        if incorrect_chars:
            raise InvalidAPIUsage(INVALID_CUSTOM_ID)
        if cls.get_original_link(short):
            raise InvalidAPIUsage(SHORT_LINK_EXIST_MESSAGE_API.format(short))
        return original, short

    @staticmethod
    def get_unique_short_id():
        for _ in range(ATTEMPTS_COUNT):
            short_id = ''.join(
                random.choices(AVAILABLE_CHARS, k=ID_MAX_LENGTH))
            if not URLMap.query.filter_by(short=short_id).first():
                return short_id
        raise ValueError(SHORT_ID_NOT_FOUND_MESSAGE)

    @staticmethod
    def get_original_link_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404().original

    @staticmethod
    def get_original_link(short):
        return URLMap.query.filter_by(short=short).first()
