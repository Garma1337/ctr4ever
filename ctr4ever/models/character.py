# coding=utf-8

from typing import List

from marshmallow import Schema, fields
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.model import Model


class CharacterSchema(Schema):
    id = fields.Int()
    engine_style_id = fields.Int()
    name = fields.Str()
    icon = fields.Str()
    engine_style = fields.Nested('EngineStyleSchema', exclude=('characters',))
    submissions = fields.Nested('SubmissionSchema', exclude=('character',), many=True)


class Character(Model):
    __tablename__ = 'characters'
    __dump_schema__ = CharacterSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    engine_style_id: Mapped[int] = Column(ForeignKey('engine_styles.id'))
    name: Mapped[str] = Column(String(100), nullable=False)
    icon: Mapped[str] = Column(String(100), nullable=False)
    engine_style: Mapped['EngineStyle'] = relationship('EngineStyle', back_populates='characters')
    submissions: Mapped[List['Submissions']] = relationship('Submission', back_populates='character')
