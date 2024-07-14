# coding=utf-8

from typing import List, Optional

from ctr4ever.models.gameversion import GameVersion
from ctr4ever.models.repository.modelrepository import ModelRepository


class GameVersionRepository(ModelRepository):

    def find_by(self, name: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> List[GameVersion]:
        return super().find_by(name=name, limit=limit, offset=offset)

    def count(self, name: Optional[str] = None) -> int:
        return super().count(name=name)

    def create(self, name: str, icon: str) -> GameVersion:
        return super().create(name=name, icon=icon)

    def update(self, id: int, name: Optional[str] = None, icon: Optional[str] = None) -> None:
        super().update(id=id, name=name, icon=icon)

    def _get_model_class(self) -> type:
        return GameVersion
