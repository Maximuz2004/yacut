from re import sub

from datetime import datetime
import random

from flask import url_for

from . import db
from .constants import (
    ATTEMPTS_COUNT, AVAILABLE_CHARS, AVAILABLE_CHARS_REGEX, SHORT_MAX_LENGTH,
    REDIRECT_VIEW,
    SHORT_ID_NOT_FOUND_MESSAGE, URL_MAX_LENGTH
)

SHORT_LINK_EXIST_MESSAGE_API = 'Имя "{}" уже занято.'
INVALID_SHORT = ('Указано недопустимое имя для короткой ссылки')
INVALID_ORIGINAL_LINK_LENGTH = (f'Ссылка не может быть длинной больше чем'
                                f' {URL_MAX_LENGTH} символов')


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(URL_MAX_LENGTH),
        nullable=False,
        index=True,
    )
    short = db.Column(
        db.String(SHORT_MAX_LENGTH),
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

    @staticmethod
    def create(original, short=None, validate_api=True):
        if short is None or short == '':
            short = URLMap.get_unique_short_id()
        elif validate_api:
            short_length = len(short)
            if short_length > SHORT_MAX_LENGTH:
                raise ValueError(INVALID_SHORT)
            incorrect_chars = sub(AVAILABLE_CHARS_REGEX, '', short)
            if incorrect_chars:
                raise ValueError(INVALID_SHORT)
            if URLMap.get_url_map(short):
                raise ValueError(SHORT_LINK_EXIST_MESSAGE_API.format(short))
        original_length = len(original)
        if original_length > URL_MAX_LENGTH:
            raise ValueError(
                INVALID_ORIGINAL_LINK_LENGTH.format(
                    current_length=original_length
                )
            )
        instance = URLMap(original=original, short=short)
        db.session.add(instance)
        db.session.commit()
        return instance

    @staticmethod
    def get_unique_short_id():
        for _ in range(ATTEMPTS_COUNT):
            short = ''.join(
                random.choices(AVAILABLE_CHARS, k=SHORT_MAX_LENGTH))
            if not URLMap.get_url_map(short):
                return short
        raise ValueError(SHORT_ID_NOT_FOUND_MESSAGE)

    @staticmethod
    def get_original_link_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404().original

    @staticmethod
    def get_url_map(short):
        return URLMap.query.filter_by(short=short).first()
