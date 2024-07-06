# coding=utf-8

from flask_sqlalchemy import SQLAlchemy


class FakerService(object):

    def __init__(self, db: SQLAlchemy):
        self.db = db

    def generate_fake_players(self):
        pass

    def generate_fake_submissions(self):
        pass
