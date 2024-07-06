# coding=utf-8

from typing import List

from marshmallow import Schema, fields
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.modelbase import ModelBase


class CategorySchema(Schema):

    id = fields.Int()
    name = fields.Str()
    standard_times = fields.Nested('StandardTimeSchema', exclude=('category',), many=True)
    submissions = fields.Nested('SubmissionSchema', exclude=('category',), many=True)


class Category(ModelBase):

    __tablename__ = 'categories'
    __dump_schema__ = CategorySchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    standard_times: Mapped[List['StandardTime']] = relationship('StandardTime', back_populates='category')
    submissions: Mapped[List['Submission']] = relationship('Submission', back_populates='category')