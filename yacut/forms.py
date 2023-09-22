from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired, Length, Optional, Regexp, URL, ValidationError
)

from .constants import (
    ID_MAX_LENGTH, INVALID_ORIGINAL_LINK_MESSAGE, INVALID_SHORT_MESSAGE,
    ORIGINAL_LABEL, REQUIRED_FIELD_MESSAGE, SHORT_LABEL,
    SHORT_LINK_EXIST_MESSAGE, SHORT_PATTERN, SUBMIT_LABEL, URL_MAX_LENGTH
)
from .models import URLMap


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
            Length(max=ID_MAX_LENGTH),
            Regexp(
                SHORT_PATTERN,
                message=INVALID_SHORT_MESSAGE
            ),
            Optional()
        ]
    )
    submit = SubmitField(SUBMIT_LABEL)

    def validate_custom_id(self, custom_id):
        short = custom_id.data
        if URLMap.get_original_link(short):
            raise ValidationError(SHORT_LINK_EXIST_MESSAGE.format(short))
