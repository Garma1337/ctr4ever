# coding=utf-8

from typing import List, Optional

from ctr4ever.models.repository.modelrepository import ModelRepository
from ctr4ever.models.ruleset import Ruleset


class RulesetRepository(ModelRepository):

    def find_by(self, name: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> List[Ruleset]:
        return super().find_by(name=name, limit=limit, offset=offset)

    def count(self, name: Optional[str] = None) -> int:
        return super().count(name=name)

    def create(self, name: str) -> Ruleset:
        return super().create(name=name)

    def update(self, id: int, name: Optional[str] = None) -> None:
        super().update(id=id, name=name)

    def _get_model_class(self) -> type:
        return Ruleset
