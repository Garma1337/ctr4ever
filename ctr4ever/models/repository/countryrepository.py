# coding=utf-8

from typing import List, Optional

from ctr4ever.models.country import Country
from ctr4ever.models.repository.modelrepository import ModelRepository


class CountryRepository(ModelRepository):

    def find_by(self, name: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> List[Country]:
        return super().find_by(name=name, limit=limit, offset=offset)

    def count(self, name: Optional[str] = None) -> int:
        return super().count(name=name)

    def create(self, name: str, flag: str) -> Country:
        return super().create(name=name, flag=flag)

    def update(self, id: int, name: Optional[str] = None) -> None:
        super().update(id=id, name=name)

    def _get_model_class(self) -> type:
        return Country
