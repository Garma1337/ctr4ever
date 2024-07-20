# coding=utf-8

import os

from ctr4ever import db

DATABASE_DRIVER = os.getenv('DATABASE_DRIVER')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')

SQLALCHEMY_DATABASE_URI = f'{DATABASE_DRIVER}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

SESSION_SQLALCHEMY = db
SESSION_TYPE = os.getenv('SESSION_TYPE')
SESSION_SQLALCHEMY_TABLE = os.getenv('SESSION_SQLALCHEMY_TABLE')
