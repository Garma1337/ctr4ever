# coding=utf-8

import sys

from cachelib import NullCache
from flask import Flask
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

sys.dont_write_bytecode = True

db = SQLAlchemy()
migrate = Migrate()
session = Session()
talisman = Talisman()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config.from_pyfile('config.dev.py', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)
    session.init_app(app)
    talisman.init_app(app)

    from . import container
    container.init_app(app)

    from .cli.faker import faker
    from .cli.installer import installer
    from .rest.api import rest_api

    app.register_blueprint(faker)
    app.register_blueprint(installer)
    app.register_blueprint(rest_api)

    return app

def create_test_app() -> Flask:
    """
    This app factory is only used for integration testing. It is not used in production.
    :return: The flask test app
    """
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config.from_pyfile('config.dev.py', silent=True)

    app.config.from_mapping({
        'SESSION_TYPE': 'cachelib',
        'SESSION_CACHELIB': NullCache(),
    })

    db.init_app(app)
    migrate.init_app(app, db)
    session.init_app(app)

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
