# coding=utf-8

from unittest import TestCase

from ctr4ever.services.validator.categoryvalidator import CategoryValidator
from ctr4ever.services.validator.validator import ValidationError
from ctr4ever.tests.mockmodelrepository import MockCategoryRepository


class CategoryValidatorTest(TestCase):

    def setUp(self):
        self.category_repository = MockCategoryRepository()
        self.category_validator = CategoryValidator(self.category_repository)

    def test_can_validate_category_name(self):
        self.category_validator.validate_name('Course')

    def test_can_not_validate_empty_category_name(self):
        with self.assertRaises(ValidationError):
            self.category_validator.validate_name('')

    def test_can_not_validate_existing_category_name(self):
        self.category_repository.create('Course')

        with self.assertRaises(ValidationError):
            self.category_validator.validate_name('Course')

    def test_can_validate_category_id(self):
        category = self.category_repository.create('Course')

        self.category_validator.validate_id(category.id)

    def test_can_not_validate_empty_category_id(self):
        with self.assertRaises(ValidationError):
            self.category_validator.validate_id(None)

    def test_can_not_validate_nonexistent_category_id(self):
        with self.assertRaises(ValidationError):
            self.category_validator.validate_id(1)
