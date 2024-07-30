# coding=utf-8

from ctr4ever.models.repository.gameversionrepository import GameVersionRepository
from ctr4ever.services.validator.validator import Validator, ValidationError


class GameVersionValidator(Validator):

    def __init__(self, game_version_repository: GameVersionRepository):
        self.game_version_repository = game_version_repository

    def validate_game_version(self, name):
        self.validate_name(name)

    def validate_name(self, name):
        if not name:
            raise ValidationError('The game version name cannot be empty.')

        existing_game_versions = self.game_version_repository.find_by(name=name)

        if len(existing_game_versions) > 0:
            raise ValidationError(f'A game version with the name "{name}" already exists.')

    def validate_id(self, game_version_id):
        if not game_version_id:
            raise ValidationError('The game version id cannot be empty.')

        game_version = self.game_version_repository.find_one(game_version_id)

        if not game_version:
            raise ValidationError(f'No game version with the id "{game_version_id}" exists.')
