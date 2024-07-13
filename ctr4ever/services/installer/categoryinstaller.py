# coding=utf-8

import json
import os
from typing import List

from ctr4ever.models.category import Category
from ctr4ever.models.repository.categoryrepository import CategoryRepository
from ctr4ever.services.installer.installer import Installer


class CategoryInstaller(Installer):

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def install(self, file_name: str):
        if not os.path.exists(file_name):
            raise ValueError(f'File "{file_name}" does not exist')

        with open(file_name) as file_pointer:
            json_content = json.loads(file_pointer.read())
            categories = self._parse_categories(json_content)
            self._create_categories(categories)

    def _create_categories(self, categories: List[Category]):
        for category in categories:
            result = self.category_repository.find_by(category.name)

            if len(result) > 0:
                existing_category = result[0]
                self.category_repository.update(id=existing_category.id, name=category.name)
            else:
                self.category_repository.create(category.name)

    def _parse_categories(self, json_content: list[dict]) -> List[Category]:
        categories: List[Category] = []

        for entry in json_content:
            if not 'name' in entry or not entry['name']:
                raise ValueError('Category name is required')

            categories.append(Category(name=entry['name']))

        return categories
