# coding=utf-8

from typing import List, Optional

from ctr4ever.models.repository.modelrepository import ModelRepository
from ctr4ever.models.standard import Standard


class StandardRepository(ModelRepository):

    def find_by(self, name: Optional[str] = None) -> List[Standard]:
        return super().find_by(name = name)

    def create(self, name: str, calculator_class: str) -> Standard:
        return super().create(name = name, calculator_class = calculator_class)

    def _get_model_class(self) -> type:
        return Standard
