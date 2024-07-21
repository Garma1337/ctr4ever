# coding=utf-8

from typing import Optional
from unittest import TestCase

from flask import Flask
from flask_migrate import upgrade
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from ctr4ever import create_test_app, db
from ctr4ever.helpers.filesystem import FileSystem


class IntegrationTest(TestCase):
    """
    Integration tests use actual external dependencies instead of mocking them. In the case of ctr4ever, it's mainly
    the database and some other objects like the session.
    """

    app: Optional[Flask] = None
    db: Optional[SQLAlchemy] = None

    @classmethod
    def setUpClass(cls):
        cls.app = create_test_app()
        cls.db = db

        with cls.app.app_context():
            cls.db.session.execute(text(f'DROP SCHEMA public CASCADE'))
            cls.db.session.execute(text(f'CREATE SCHEMA public'))
            cls.db.session.execute(text(f'GRANT ALL ON SCHEMA public TO {cls.app.config["DATABASE_USER"]}'))
            cls.db.session.commit()
            upgrade(directory= f'{FileSystem.get_current_directory()}/../../migrations')

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            cls.db.session.rollback()
            cls.db.session.close()

        cls.db = None
        cls.app = None
