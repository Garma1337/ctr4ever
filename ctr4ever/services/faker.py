# coding=utf-8

from flask_sqlalchemy import SQLAlchemy


class Faker(object):

    def __init__(self, db: SQLAlchemy):
        self.db = db

    def generate_fake_players(self, count: int):
        for i in range(count):
            pass

    def generate_fake_submissions(self, count):
        for i in range(count):
            pass
