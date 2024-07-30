# coding=utf-8

from unittest import TestCase

from ctr4ever.services.validator.charactervalidator import CharacterValidator
from ctr4ever.services.validator.validator import ValidationError
from ctr4ever.tests.mockmodelrepository import MockCharacterRepository, MockEngineStyleRepository


class CharacterValidatorTest(TestCase):

    def setUp(self):
        self.character_repository = MockCharacterRepository()
        self.engine_style_repository = MockEngineStyleRepository()
        self.character_validator = CharacterValidator(self.character_repository, self.engine_style_repository)

    def test_can_validate_character_name(self):
        self.character_validator.validate_name('Crash')

    def test_can_not_validate_empty_character_name(self):
        with self.assertRaises(ValidationError):
            self.character_validator.validate_name('')

    def test_can_not_validate_existing_character_name(self):
        self.character_repository.create('Crash', 1, 'crash.png')

        with self.assertRaises(ValidationError):
            self.character_validator.validate_name('Crash')

    def test_can_validate_engine_style(self):
        engine_style = self.engine_style_repository.create('Speed')

        self.character_validator.validate_engine_style(engine_style.id)

    def test_can_not_validate_empty_engine_style(self):
        with self.assertRaises(ValidationError):
            self.character_validator.validate_engine_style(None)

    def test_can_not_validate_nonexistent_engine_style(self):
        with self.assertRaises(ValidationError):
            self.character_validator.validate_engine_style(1)

    def test_can_validate_character_id(self):
        character = self.character_repository.create('Crash', 1, 'crash.png')

        self.character_validator.validate_id(character.id)

    def test_can_not_validate_empty_character_id(self):
        with self.assertRaises(ValidationError):
            self.character_validator.validate_id(None)

    def test_can_not_validate_nonexistent_character_id(self):
        with self.assertRaises(ValidationError):
            self.character_validator.validate_id(1)
