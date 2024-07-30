# coding=utf-8

from unittest import TestCase

from ctr4ever.services.validator.enginestylevalidator import EngineStyleValidator
from ctr4ever.services.validator.validator import ValidationError
from ctr4ever.tests.mockmodelrepository import MockEngineStyleRepository


class EngineStyleValidatorTest(TestCase):

    def setUp(self):
        self.engine_style_repository = MockEngineStyleRepository()
        self.engine_style_validator = EngineStyleValidator(self.engine_style_repository)

    def test_can_validate_engine_style_name(self):
        self.engine_style_validator.validate_name('Speed')

    def test_can_not_validate_empty_engine_style_name(self):
        with self.assertRaises(ValidationError):
            self.engine_style_validator.validate_name('')

    def test_can_not_validate_existing_engine_style_name(self):
        self.engine_style_repository.create('Speed')

        with self.assertRaises(ValidationError):
            self.engine_style_validator.validate_name('Speed')

    def test_can_validate_engine_style_id(self):
        engine_style = self.engine_style_repository.create('Speed')

        self.engine_style_validator.validate_id(engine_style.id)

    def test_can_not_validate_empty_engine_style_id(self):
        with self.assertRaises(ValidationError):
            self.engine_style_validator.validate_id(None)

    def test_can_not_validate_nonexistent_engine_style_id(self):
        with self.assertRaises(ValidationError):
            self.engine_style_validator.validate_id(1)
