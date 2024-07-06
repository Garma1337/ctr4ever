# coding=utf-8

from typing import Optional, List

from ctr4ever.models.player import Player
from ctr4ever.models.repository.modelrepository import ModelRepository


class PlayerRepository(ModelRepository):

    def find_by(self, name: Optional[str] = None) -> List[Player]:
        return super().find_by(name=name)

    def create(self, name: str, email: str, country_id: int) -> Player:
        return self.create(
            name=name,
            email=email,
            country_id=country_id
        )

    def _get_model_class(self) -> type:
        return Player
