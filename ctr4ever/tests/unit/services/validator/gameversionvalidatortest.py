# coding=utf-8

from unittest import TestCase

from ctr4ever.services.validator.gameversionvalidator import GameVersionValidator
from ctr4ever.services.validator.validator import ValidationError
from ctr4ever.tests.mockmodelrepository import MockGameVersionRepository


class GameVersionValidatorTest(TestCase):

    def setUp(self):
        self.game_version_repository = MockGameVersionRepository()
        self.game_version_validator = GameVersionValidator(self.game_version_repository)

    def test_can_validate_game_version_name(self):
        self.game_version_validator.validate_name('PAL')

    def test_can_not_validate_empty_game_version_name(self):
        with self.assertRaises(ValidationError):
            self.game_version_validator.validate_name('')

    def test_can_not_validate_existing_game_version_name(self):
        self.game_version_repository.create('PAL', 'pal.png')

        with self.assertRaises(ValidationError):
            self.game_version_validator.validate_name('PAL')

    def test_can_validate_game_version_id(self):
        game_version = self.game_version_repository.create('PAL', 'pal.png')

        self.game_version_validator.validate_id(game_version.id)

    def test_can_not_validate_empty_game_version_id(self):
        with self.assertRaises(ValidationError):
            self.game_version_validator.validate_id(None)

    def test_can_not_validate_nonexistent_game_version_id(self):
        with self.assertRaises(ValidationError):
            self.game_version_validator.validate_id(1)
