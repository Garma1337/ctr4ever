# coding=utf-8

from abc import ABC, abstractmethod

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update

from ctr4ever.models.model import Model


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
                if arg == 'limit':
                    query.limit(kwargs[arg])
                elif arg == 'offset':
                    query.offset(kwargs[arg])
                else:
                    query.where(getattr(self._model_class, arg) == kwargs[arg])

        return query.all()

    def count(self, **kwargs) -> int:
        query = self._db.session.query(self._model_class)

        for arg in kwargs:
            if kwargs[arg] is not None:
                query.where(getattr(self._model_class, arg) == kwargs[arg])

        return query.count()

    def create(self, **kwargs) -> Model:
        self._db.session.begin()

        model = self._model_class(**kwargs)
        self._db.session.add(model)

        self._db.session.commit()
        self._db.session.flush()

        return model

    def update(self, **kwargs) -> None:
        if not 'id' in kwargs:
            raise ValueError('An id is required to update an entity')

        self._db.session.begin()

        values = [kwarg for kwarg in kwargs if kwarg != 'id' and kwargs[kwarg] is not None]

        for attribute in values:
            if not hasattr(self._model_class, attribute):
                raise ValueError(f'Entity {self._model_class.__name__} has attribute {attribute}')

        statement = (
            update(self._model_class)
            .where(getattr(self._model_class, 'id').in_([kwargs['id']]))
            .values(**values)
        )

        self._db.session.execute(statement)

        self._db.session.commit()
        self._db.session.flush()

    @abstractmethod
    def _get_model_class(self) -> type:
        pass
