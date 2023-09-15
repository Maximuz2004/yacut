from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

MIN_LENGTH = 1
ID_MAX_LENGTH = 6
URL_MAX_LENGTH = 2048

from . import api_views, views
