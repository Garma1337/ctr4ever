# coding=utf-8

from typing import List

from marshmallow import Schema, fields
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever import db


class RulesetSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    submissions = fields.Nested('SubmissionSchema', exclude=('ruleset',), many=True)


class Ruleset(db.Model):
    __tablename__ = 'rulesets'
    __dump_schema__ = RulesetSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = Column(String(50))
    submissions: Mapped[List['Submission']] = relationship('Submission', back_populates='ruleset')
