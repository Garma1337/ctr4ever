# coding=utf-8

from ctr4ever.models.repository.categoryrepository import CategoryRepository
from ctr4ever.services.validator.validator import ValidationError, Validator


class CategoryValidator(Validator):

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def validate_category(self, name: str):
        self.validate_name(name)

    def validate_name(self, name: str):
        if not name:
            raise ValidationError('The category name cannot be empty.')

        existing_categories = self.category_repository.find_by(name=name)

        if len(existing_categories) > 0:
            raise ValidationError(f'A category with the name "{name}" already exists.')

    def validate_id(self, category_id: int):
        if not category_id:
            raise ValidationError('The category id cannot be empty.')

        category = self.category_repository.find_one(category_id)

        if not category:
            raise ValidationError(f'No category with the id "{category_id}" exists.')
