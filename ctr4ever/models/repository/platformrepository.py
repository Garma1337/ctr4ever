# coding=utf-8

from typing import List

from ctr4ever.models.platform import Platform
from ctr4ever.models.repository.modelrepository import ModelRepository


class PlatformRepository(ModelRepository):

    def find_by(self, name: str) -> List[Platform]:
        return super().find_by(name=name)

    def create(self, name: str) -> Platform:
        return super().create(name=name)

    def update(self, id: int, name: str) -> None:
        super().update(id=id, name=name)

    def _get_model_class(self) -> type:
        return Platform
