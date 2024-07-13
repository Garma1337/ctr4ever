# coding=utf-8

from typing import List

from ctr4ever.models.repository.modelrepository import ModelRepository
from ctr4ever.models.ruleset import Ruleset


class RulesetRepository(ModelRepository):

    def find_by(self, name: str) -> List[Ruleset]:
        return super().find_by(name=name)

    def create(self, name: str) -> Ruleset:
        return super().create(name=name)

    def update(self, id: int, name: str) -> None:
        super().update(id=id, name=name)

    def _get_model_class(self) -> type:
        return Ruleset
