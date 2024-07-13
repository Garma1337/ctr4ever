# coding=utf-8

import sys

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

sys.dont_write_bytecode = True

db = SQLAlchemy()
migrate = Migrate()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config.from_pyfile('config.dev.py', silent=True)

    app.secret_key = app.config.get('APP_SECRET_KEY')

    db.init_app(app)
    migrate.init_app(app, db)

    from . import container
    container.init_app(app)

    from .cli.faker import faker
    from .cli.installer import installer
    from .rest.api import rest_api

    app.register_blueprint(faker)
    app.register_blueprint(installer)
    app.register_blueprint(rest_api)

    return app

from ctr4ever.models import (
    gameversion,
    track,
    player,
    country,
    category,
    standard,
    character,
    submission,
    standardtime,
    enginestyle,
    standardset,
    ruleset,
    platform
)
