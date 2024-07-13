# coding=utf-8

from typing import List, Optional

from ctr4ever.models.repository.modelrepository import ModelRepository
from ctr4ever.models.standard import Standard


class StandardRepository(ModelRepository):

    def find_by(self, name: Optional[str] = None, standard_set_id: Optional[int] = None) -> List[Standard]:
        return super().find_by(name=name, standard_set_id=standard_set_id)

    def create(self, name: str, standard_set_id: int) -> Standard:
        return super().create(name=name, standard_set_id=standard_set_id)

    def update(
            self,
            id: int,
            name: Optional[str] = None,
            standard_set_id: Optional[int] = None
    ) -> None:
        super().update(id=id, name=name, standard_set_id=standard_set_id)

    def _get_model_class(self) -> type:
        return Standard
