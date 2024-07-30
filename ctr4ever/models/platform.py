# coding=utf-8

from typing import List

from marshmallow import Schema, fields
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.model import Model


class PlatformSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    submissions = fields.Nested('SubmissionSchema', exclude=('platform',), many=True)
    submissions_history = fields.Nested('SubmissionHistorySchema', exclude=('platform',), many=True)


class Platform(Model):
    __tablename__ = 'platforms'
    __dump_schema__ = PlatformSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    submissions: Mapped[List['Submission']] = relationship('Submission', back_populates='platform')
    submissions_history: Mapped[List['SubmissionHistory']] = relationship('SubmissionHistory', back_populates='platform')
