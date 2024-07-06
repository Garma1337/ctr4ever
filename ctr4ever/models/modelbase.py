# coding=utf-8

import json

from marshmallow import Schema

from ctr4ever import db


class ModelBase(db.Model):

    __abstract__: bool = True
    __dump_schema__: Schema = None

    def to_dictionary(self):
        if not self.__dump_schema__:
            return {}

        return self.__dump_schema__.dump(self)

    def to_json(self):
        return json.dumps(self.to_dictionary())
