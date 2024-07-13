# coding=utf-8

from typing import List

from marshmallow import Schema, fields
from sqlalchemy import String, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.model import Model


class EngineStyleSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    characters = fields.Nested('CharacterSchema', exclude=('engine_style',), many=True)


class EngineStyle(Model):
    __tablename__ = 'engine_styles'
    __dump_schema__ = EngineStyleSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = Column(String(100), unique=True, nullable=False)
    characters: Mapped[List['Character']] = relationship('Character', back_populates='engine_style')
