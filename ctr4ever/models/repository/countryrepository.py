# coding=utf-8

from typing import List

from ctr4ever.models.country import Country
from ctr4ever.models.repository.modelrepository import ModelRepository


class CountryRepository(ModelRepository):

    def find_by(self, name: str) -> List[Country]:
        return super().find_by(name = name)

    def create(self, name: str) -> Country:
        return super().create(name = name)

    def _get_model_class(self) -> type:
        return Country
