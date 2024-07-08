# coding=utf-8

from typing import List

from ctr4ever.models.character import Character
from ctr4ever.models.repository.modelrepository import ModelRepository


class CharacterRepository(ModelRepository):

    def find_by(self, name: str) -> List[Character]:
        return super().find_by(name = name)

    def create(self, name: str, engine_style_id: int, icon: str) -> Character:
        return super().create(
            name = name,
            engine_style_id = engine_style_id,
            icon = icon
        )

    def _get_model_class(self) -> type:
        return Character
