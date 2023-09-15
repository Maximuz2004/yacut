from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from yacut import ID_MAX_LENGTH, MIN_LENGTH, URL_MAX_LENGTH

LONG_URL_LABBEL = 'Длинная ссылка'
ID_LABEL = 'Ваш вариант короткой ссылки'
ID_VALIDATION_PATTERN = r'^[a-zA-Z0-9]+$'
INVALID_VALIDATION_MESSAGE = ('Короткая ссылка может содержать только '
                              'латинские  буквы и цифры в диапазоне от 0 до 9')
REQUIRED_FIELD_MESSAGE = 'Обязательное поле'
SUBMIT_LABEL = 'Создать'


class URLMapForm(FlaskForm):
    original_link = URLField(
        LONG_URL_LABBEL,
        validators=[
            DataRequired(message=REQUIRED_FIELD_MESSAGE),
            Length(MIN_LENGTH, URL_MAX_LENGTH)
        ]
    )
    custom_id = StringField(
        ID_LABEL,
        validators=[
            Length(MIN_LENGTH, ID_MAX_LENGTH),
            Regexp(
                ID_VALIDATION_PATTERN,
                message=INVALID_VALIDATION_MESSAGE
            ),
            Optional()
        ]
    )
    submit = SubmitField(SUBMIT_LABEL)
