# coding=utf-8

from typing import List

from ctr4ever.models.enginestyle import EngineStyle
from ctr4ever.models.repository.modelrepository import ModelRepository


class EngineStyleRepository(ModelRepository):

    def find_by(self, name: str) -> List[EngineStyle]:
        return super().find_by(name=name)

    def create(self, name: str) -> EngineStyle:
        return super().create(name=name)

    def update(self, id: int, name: str) -> None:
        super().update(id=id, name=name)

    def _get_model_class(self) -> type:
        return EngineStyle
