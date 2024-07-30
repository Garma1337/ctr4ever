# coding=utf-8

from ctr4ever.models.repository.characterrepository import CharacterRepository
from ctr4ever.models.repository.enginestylerepository import EngineStyleRepository
from ctr4ever.services.validator.validator import Validator, ValidationError


class CharacterValidator(Validator):

    def __init__(self, character_repository: CharacterRepository, engine_style_repository: EngineStyleRepository):
        self.character_repository = character_repository
        self.engine_style_repository = engine_style_repository

    def validate_character(self, name: str, engine_style_id: int):
        self.validate_name(name)
        self.validate_engine_style(engine_style_id)

    def validate_name(self, name: str):
        if not name:
            raise ValidationError('The character name cannot be empty.')

        existing_characters = self.character_repository.find_by(name=name)

        if len(existing_characters) > 0:
            raise ValidationError(f'A character with the name "{name}" already exists.')

    def validate_engine_style(self, engine_style_id: int):
        if not engine_style_id:
            raise ValidationError('The engine style id cannot be empty.')

        engine_style = self.engine_style_repository.find_one(engine_style_id)

        if not engine_style:
            raise ValidationError(f'No engine style with the id "{engine_style_id}" exists.')

    def validate_id(self, character_id: int):
        if not character_id:
            raise ValidationError('The character id cannot be empty.')

        character = self.character_repository.find_one(character_id)

        if not character:
            raise ValidationError(f'No character with the id "{character_id}" exists.')
