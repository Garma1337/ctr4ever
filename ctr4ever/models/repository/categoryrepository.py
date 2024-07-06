# coding=utf-8

from typing import List

from ctr4ever.models.category import Category
from ctr4ever.models.repository.modelrepository import ModelRepository


class CategoryRepository(ModelRepository):

    def find_by(self, name: str) -> List[Category]:
        return super().find_by(name = name)

    def create(self, name: str) -> Category:
        return super().create(name = name)

    def _get_model_class(self) -> type:
        return Category
