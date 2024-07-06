# coding=utf-8

from typing import List

from marshmallow import Schema, fields
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.modelbase import ModelBase


class CharacterSchema(Schema):

    id = fields.Int()
    name = fields.Str()
    icon = fields.Str()
    submissions = fields.Nested('SubmissionSchema', exclude=('character',), many=True)


class Character(ModelBase):

    __tablename__ = 'characters'
    __dump_schema__ = CharacterSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    icon: Mapped[str] = Column(String(100), nullable=False)
    submissions: Mapped[List['Submissions']] = relationship('Submission', back_populates='character')
