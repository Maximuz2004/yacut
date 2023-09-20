from datetime import datetime

from flask import url_for

from . import db
from .constants import ID_MAX_LENGTH, URL_MAX_LENGTH


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
                'redirect_view',
                custom_id=self.short,
                _external=True
            )
        )

    def from_dict(self, data):
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])
