# coding=utf-8

from typing import List

from marshmallow import Schema, fields
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.modelbase import ModelBase


class PlayerSchema(Schema):

    id = fields.Int()
    name = fields.Str()
    country_id = fields.Int()
    country = fields.Nested('CountrySchema', exclude=('players',))
    submissions = fields.Nested('SubmissionSchema', exclude=('player',), many=True)


class Player(ModelBase):

    __tablename__ = 'players'
    __dump_schema__ = PlayerSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id'))
    name: Mapped[str] = Column(String(100), nullable=False)
    email: Mapped[str] = Column(String(255), unique=True, nullable=False)
    password: Mapped[str] = Column(String(255), nullable=False)
    country: Mapped['Country'] = relationship('Country', back_populates='players')
    submissions: Mapped[List['Submission']] = relationship('Submission', back_populates='player')