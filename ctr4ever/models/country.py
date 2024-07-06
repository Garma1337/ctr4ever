# coding=utf-8

from typing import List

from marshmallow import Schema, fields
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.modelbase import ModelBase


class CountrySchema(Schema):

    id = fields.Int()
    name = fields.Str()
    flag = fields.Str()
    players = fields.Nested('PlayerSchema', exclude=('country',), many=True)


class Country(ModelBase):

    __tablename__ = 'countries'
    __dump_schema__ = CountrySchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = Column(String(100), unique=True, nullable=False)
    flag: Mapped[str] = Column(String(100), nullable=False)
    players: Mapped[List['Player']] = relationship('Player', back_populates='country')
