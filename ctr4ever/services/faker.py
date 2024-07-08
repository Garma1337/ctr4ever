# coding=utf-8

from flask_sqlalchemy import SQLAlchemy


class Faker(object):

    def __init__(self, db: SQLAlchemy):
        self.db = db

    def generate_fake_countries(self):
        pass

    def generate_fake_players(self):
        pass

    def generate_fake_submissions(self):
        pass
