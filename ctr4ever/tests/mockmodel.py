# coding=utf-8

from marshmallow import Schema
from sqlalchemy.orm import mapped_column, Mapped, declarative_base

from ctr4ever import db
from ctr4ever.models.repository.modelrepository import ModelRepository


Base = declarative_base()


class MockSchema(Schema):
    pass


class MockModel(Base):

    __tablename__ = 'mock'
    __dump_schema__ = MockSchema()

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    value = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)


class MockModelRepository(ModelRepository):

    def _get_model_class(self):
        return MockModel
