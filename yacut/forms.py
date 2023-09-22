from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired, Length, Optional, Regexp, URL, ValidationError
)

from .constants import (
    AVAILABLE_CHARS_REGEX, SHORT_MAX_LENGTH, URL_MAX_LENGTH
)
from .models import URLMap

ORIGINAL_LABEL = 'Длинная ссылка'
SHORT_LABEL = 'Ваш вариант короткой ссылки'
INVALID_ORIGINAL_LINK_MESSAGE = 'Некорректная длинная ссылка'
INVALID_SHORT_MESSAGE = ('Короткая ссылка может содержать только '
                         'латинские  буквы и цифры в диапазоне от 0 до 9')
REQUIRED_FIELD_MESSAGE = 'Обязательное поле'
SUBMIT_LABEL = 'Создать'
SHORT_LINK_EXIST_MESSAGE = 'Имя {} уже занято!'


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LABEL,
        validators=[
            DataRequired(message=REQUIRED_FIELD_MESSAGE),
            Length(max=URL_MAX_LENGTH),
            URL(message=INVALID_ORIGINAL_LINK_MESSAGE)
        ]
    )
    custom_id = StringField(
        SHORT_LABEL,
        validators=[
            Length(max=SHORT_MAX_LENGTH),
            Regexp(
                AVAILABLE_CHARS_REGEX,
                message=INVALID_SHORT_MESSAGE
            ),
            Optional()
        ]
    )
    submit = SubmitField(SUBMIT_LABEL)

    def validate_custom_id(self, custom_id):
        short = custom_id.data
        if URLMap.get_url_map(short):
            raise ValidationError(SHORT_LINK_EXIST_MESSAGE.format(short))
