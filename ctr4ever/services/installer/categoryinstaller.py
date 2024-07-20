# coding=utf-8

from typing import List

from ctr4ever.models.category import Category
from ctr4ever.models.repository.categoryrepository import CategoryRepository
from ctr4ever.services.installer.installer import Installer


class CategoryInstaller(Installer):

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def _validate_entry(self, entry: dict):
        if not 'name' in entry or not entry['name']:
            raise ValueError('Category name is required')

    def _parse_json(self, json_content: list[dict]) -> List[Category]:
        categories: List[Category] = []

        for entry in json_content:
            categories.append(Category(name=entry['name']))

        return categories

    def _create_entries(self, categories: List[Category]) -> None:
        for category in categories:
            result = self.category_repository.find_by(category.name)

            if len(result) > 0:
                existing_category = result[0]
                self.category_repository.update(id=existing_category.id, name=category.name)
            else:
                self.category_repository.create(category.name)
