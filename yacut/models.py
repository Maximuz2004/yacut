from datetime import datetime

from yacut import db, ID_MAX_LENGTH, URL_MAX_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(URL_MAX_LENGTH),
        nullable=False,
        unique=True
    )
    short = db.Column(
        db.String(ID_MAX_LENGTH),
        nullable=False,
        unique=True
    )
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow
    )
