# coding=utf-8

from typing import List

from marshmallow import Schema, fields
from marshmallow.fields import Nested
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.model import Model


class StandardSchema(Schema):

    id = fields.Int()
    name = fields.Str()
    standard_set = fields.Nested('StandardSetSchema', exclude=('standards',))
    times = Nested('StandardTimeSchema', exclude=('standard',), many=True)


class Standard(Model):

    __tablename__ = 'standards'
    __dump_schema__ = StandardSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    standard_set_id: Mapped[int] = Column(ForeignKey('standard_set.id'))
    name: Mapped[str] = Column(String(100), nullable=False)
    standard_set: Mapped['StandardSet'] = relationship('StandardSet', back_populates='standards')
    times: Mapped[List['StandardTime']] = relationship('StandardTime', back_populates='standard')
