# coding=utf-8

from typing import List

from marshmallow import Schema, fields
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.model import Model


class GameVersionSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    icon = fields.Str()
    submissions = fields.Nested('SubmissionSchema', exclude=('game_version',), many=True)
    submissions_history = fields.Nested('SubmissionHistorySchema', exclude=('game_version',), many=True)


class GameVersion(Model):
    __tablename__ = 'game_versions'
    __dump_schema__ = GameVersionSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    icon: Mapped[str] = Column(String(20), nullable=False)
    submissions: Mapped[List['Submission']] = relationship('Submission', back_populates='game_version')
    submissions_history: Mapped[List['SubmissionHistory']] = relationship('SubmissionHistory', back_populates='game_version')
