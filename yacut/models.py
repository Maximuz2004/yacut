from datetime import datetime
from re import search
import random

from flask import url_for

from . import db
from .constants import (
    ATTEMPTS_COUNT, AVAILABLE_CHARS, AVAILABLE_CHARS_REGEX, REDIRECT_VIEW,
    SHORT_MAX_LENGTH, URL_MAX_LENGTH
)

SHORT_EXIST_MESSAGE = 'Имя "{}" уже занято.'
SHORT_NOT_FOUND_MESSAGE = 'Короткая ссылка не найдена!'
INVALID_SHORT = ('Указано недопустимое имя для короткой ссылки')
INVALID_ORIGINAL_LINK_LENGTH = ('Ссылка не может быть длинной больше чем'
                                f' {URL_MAX_LENGTH} символов, ваша длинна:'
                                f' {{}} символов')


class GenerateShortError(Exception):
    pass


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
    def create(original, short=None, validate=True):
        if not short:
            short = URLMap.get_unique_short_id()
        elif validate:
            if (
                    len(short) > SHORT_MAX_LENGTH
                    or not search(AVAILABLE_CHARS_REGEX, short)
            ):
                raise ValueError(INVALID_SHORT)
            if URLMap.get(short):
                raise ValueError(SHORT_EXIST_MESSAGE.format(short))
            if (original_length := len(original)) > URL_MAX_LENGTH:
                raise ValueError(
                    INVALID_ORIGINAL_LINK_LENGTH.format(original_length)
                )
            if URLMap.get(short):
                raise ValueError(SHORT_EXIST_MESSAGE.format(short))
        instance = URLMap(original=original, short=short)
        db.session.add(instance)
        db.session.commit()
        return instance

    @staticmethod
    def get_unique_short_id():
        for _ in range(ATTEMPTS_COUNT):
            short = ''.join(
                random.choices(AVAILABLE_CHARS, k=SHORT_MAX_LENGTH))
            if not URLMap.get(short):
                return short
        raise GenerateShortError(SHORT_NOT_FOUND_MESSAGE)

    @staticmethod
    def get_original_link_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404().original

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()
