# coding=utf-8

from enum import Enum
from typing import List

from marshmallow import Schema, fields
from marshmallow.fields import Nested
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.modelbase import ModelBase

class StandardName(Enum):
    Original = 'Standards'
    Updated = 'Updated Standards'


class StandardSchema(Schema):

    id = fields.Int()
    name = fields.Str()
    times = Nested('StandardTimeSchema', exclude=('standard',), many=True)


class Standard(ModelBase):

    __tablename__ = 'standards'
    __dump_schema__ = StandardSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    times: Mapped[List['StandardTime']] = relationship('StandardTime', back_populates='standard')
