from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .constants import (ID_MAX_LENGTH, INVALID_ORIGINAL_LINK_MESSAGE,
                        INVALID_SHORT_MESSAGE, MIN_LENGTH, ORIGINAL_LABEL,
                        REQUIRED_FIELD_MESSAGE, SHORT_LABEL,
                        SHORT_PATTERN, SUBMIT_LABEL, URL_MAX_LENGTH)


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LABEL,
        validators=[
            DataRequired(message=REQUIRED_FIELD_MESSAGE),
            Length(MIN_LENGTH, URL_MAX_LENGTH),
            URL(message=INVALID_ORIGINAL_LINK_MESSAGE)
        ]
    )
    custom_id = StringField(
        SHORT_LABEL,
        validators=[
            Length(MIN_LENGTH, ID_MAX_LENGTH),
            Regexp(
                SHORT_PATTERN,
                message=INVALID_SHORT_MESSAGE
            ),
            Optional()
        ]
    )
    submit = SubmitField(SUBMIT_LABEL)
