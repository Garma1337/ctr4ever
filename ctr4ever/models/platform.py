# coding=utf-8

from typing import List

from marshmallow import Schema
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever import db


class PlatformSchema(Schema):
    pass


class Platform(db.Model):
    __tablename__ = 'platforms'
    __dump_schema__ = PlatformSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    submissions: Mapped[List['Submission']] = relationship('Submission', back_populates='platform')
