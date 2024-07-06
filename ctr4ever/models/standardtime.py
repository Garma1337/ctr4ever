# coding=utf-8

from marshmallow import Schema, fields
from marshmallow.fields import Nested
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.modelbase import ModelBase


class StandardTimeSchema(Schema):
    id = fields.Int()
    standard_id = fields.Int()
    track_id = fields.Int()
    category_id = fields.Int()
    time = fields.Str()
    numeric_value = fields.Int()
    name = fields.Str()
    standard = Nested('StandardSchema', exclude=('times',))
    track = Nested('TrackSchema', exclude=('standard_times',))
    category = Nested('CategorySchema', exclude=('standard_times',))


class StandardTime(ModelBase):

    __tablename__ = 'standards_times'
    __dump_schema__ = StandardTimeSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    standard_id: Mapped[int] = mapped_column(ForeignKey('standards.id'))
    track_id: Mapped[int] = mapped_column(ForeignKey('tracks.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    time: Mapped[str] = Column(String(20), nullable=False)
    numeric_value: Mapped[int] = Column(Integer(), nullable=False)
    name: Mapped[str] = Column(String(50), nullable=False)
    standard: Mapped['Standard'] = relationship('Standard', back_populates='times')
    track: Mapped['Track'] = relationship('Track', back_populates='standard_times')
    category: Mapped['Category'] = relationship('Category', back_populates='standard_times')
