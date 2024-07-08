# coding=utf-8

from abc import ABC, abstractmethod

from flask_sqlalchemy import SQLAlchemy

from ctr4ever.models.abstractmodel import Model


class ModelRepository(ABC):

    def __init__(self, db: SQLAlchemy) -> None:
        self._db = db
        self._model_class = self._get_model_class()

    def find_one(self, id: int):
        query = self._db.session.query(self._model_class).where(self._model_class.__getattribute__('id') == id)
        return query.first()

    def find_by(self, **kwargs):
        query = self._db.session.query(self._model_class)

        for arg in kwargs:
            if kwargs[arg] is not None:
                query.where(self._model_class.__getattribute__(arg) == kwargs[arg])

        return query.all()

    def create(self, **kwargs) -> Model:
        self._db.session.begin()

        model = self._model_class(**kwargs)
        self._db.session.add(model)

        self._db.session.commit()
        self._db.session.flush()

        return model

    @abstractmethod
    def _get_model_class(self) -> type:
        pass
