# coding=utf-8

from typing import Optional, List

from ctr4ever.models.player import Player
from ctr4ever.models.repository.modelrepository import ModelRepository


class PlayerRepository(ModelRepository):

    def find_by(
            self,
            country_id: Optional[int] = None,
            name: Optional[str] = None,
            email: Optional[str] = None,
            active: Optional[bool] = None
    ) -> List[Player]:
        return super().find_by(country_id=country_id, name=name, email=email, active=active)

    def create(self, country_id: int, name: str, email: str, password: str, salt: str, active: bool) -> Player:
        return super().create(
            country_id=country_id,
            name=name,
            email=email,
            password=password,
            salt=salt,
            active=active
        )

    def update(
            self,
            id: int,
            country_id: Optional[int] = None,
            name: Optional[str] = None,
            email: Optional[str] = None,
            password: Optional[str] = None,
            salt: Optional[str] = None,
            active: Optional[bool] = None
    ) -> None:
        super().update(
            id=id,
            country_id=country_id,
            name=name,
            email=email,
            password=password,
            salt=salt,
            active=active
        )

    def _get_model_class(self) -> type:
        return Player
