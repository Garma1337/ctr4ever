# coding=utf-8

from typing import List, Optional

from ctr4ever.models.character import Character
from ctr4ever.models.repository.modelrepository import ModelRepository


class CharacterRepository(ModelRepository):

    def find_by(self, name: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> List[Character]:
        return super().find_by(name=name, limit=limit, offset=offset)

    def count(self, name: Optional[str] = None) -> int:
        return super().count(name=name)

    def create(self, name: str, engine_style_id: int, icon: str) -> Character:
        return super().create(
            name=name,
            engine_style_id=engine_style_id,
            icon=icon
        )

    def update(self, id: int, name: Optional[str] = None, engine_style_id: Optional[int] = None, icon: Optional[str] = None) -> None:
        super().update(
            id=id,
            name=name,
            engine_style_id=engine_style_id,
            icon=icon
        )

    def _get_model_class(self) -> type:
        return Character
