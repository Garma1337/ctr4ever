# coding=utf-8

from enum import Enum
from typing import List

from marshmallow import Schema, fields
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.model import Model


class StandardSetName(Enum):
    Original = 'Standards'
    Updated = 'Updated Standards'


class StandardSetSchema(Schema):

    id = fields.Int()
    name = fields.Str()
    standards = fields.Nested('StandardSchema', exclude=('standard_set',), many=True)


class StandardSet(Model):

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = Column(String(50))
    standards: Mapped[List['Standard']] = relationship('Standard', back_populates='standard_set')
