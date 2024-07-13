# coding=utf-8

from marshmallow import Schema, fields
from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ctr4ever.models.model import Model


class StandardTimeSchema(Schema):
    id = fields.Int()
    standard_id = fields.Int()
    track_id = fields.Int()
    category_id = fields.Int()
    time = fields.Float()
    numeric_value = fields.Int()
    standard = fields.Nested('StandardSchema', exclude=('times',))
    track = fields.Nested('TrackSchema', exclude=('standard_times',))
    category = fields.Nested('CategorySchema', exclude=('standard_times',))


class StandardTime(Model):
    __tablename__ = 'standards_times'
    __dump_schema__ = StandardTimeSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    standard_id: Mapped[int] = mapped_column(ForeignKey('standards.id'))
    track_id: Mapped[int] = mapped_column(ForeignKey('tracks.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    time: Mapped[int] = Column(Float(2), nullable=False)
    numeric_value: Mapped[int] = Column(Integer(), nullable=False)
    standard: Mapped['Standard'] = relationship('Standard', back_populates='times')
    track: Mapped['Track'] = relationship('Track', back_populates='standard_times')
    category: Mapped['Category'] = relationship('Category', back_populates='standard_times')
