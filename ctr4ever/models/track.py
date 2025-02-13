# coding=utf-8

from typing import List

from marshmallow import Schema, fields
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.model import Model


class TrackSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    standard_times = fields.Nested('StandardTimeSchema', exclude=('track',), many=True)
    submissions = fields.Nested('SubmissionSchema', exclude=('track',), many=True)
    submissions_history = fields.Nested('SubmissionHistorySchema', exclude=('track',), many=True)


class Track(Model):
    __tablename__ = 'tracks'
    __dump_schema__ = TrackSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    standard_times: Mapped[List['StandardTime']] = relationship('StandardTime', back_populates='track')
    submissions: Mapped[List['Submission']] = relationship('Submission', back_populates='track')
    submissions_history: Mapped[List['SubmissionHistory']] = relationship('SubmissionHistory', back_populates='track')
