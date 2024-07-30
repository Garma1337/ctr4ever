# coding=utf-8

from unittest import TestCase

from ctr4ever.services.validator.platformvalidator import PlatformValidator
from ctr4ever.services.validator.validator import ValidationError
from ctr4ever.tests.mockmodelrepository import MockPlatformRepository


class PlatformValidatorTest(TestCase):

    def setUp(self):
        self.platform_repository = MockPlatformRepository()
        self.platform_validator = PlatformValidator(self.platform_repository)

    def test_can_validate_platform_name(self):
        self.platform_validator.validate_name('Console')

    def test_can_not_validate_empty_platform_name(self):
        with self.assertRaises(ValidationError):
            self.platform_validator.validate_name('')

    def test_can_not_validate_existing_platform_name(self):
        self.platform_repository.create('Console')

        with self.assertRaises(ValidationError):
            self.platform_validator.validate_name('Console')

    def test_can_validate_platform_id(self):
        platform = self.platform_repository.create('Console')

        self.platform_validator.validate_id(platform.id)

    def test_can_not_validate_empty_platform_id(self):
        with self.assertRaises(ValidationError):
            self.platform_validator.validate_id(None)

    def test_can_not_validate_nonexistent_platform_id(self):
        with self.assertRaises(ValidationError):
            self.platform_validator.validate_id(1)
