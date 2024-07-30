# coding=utf-8

from ctr4ever.models.repository.enginestylerepository import EngineStyleRepository
from ctr4ever.services.validator.validator import Validator, ValidationError


class EngineStyleValidator(Validator):

    def __init__(self, engine_style_repository: EngineStyleRepository):
        self.engine_style_repository = engine_style_repository

    def validate_engine_style(self, name: str):
        self.validate_name(name)

    def validate_name(self, name: str):
        if not name:
            raise ValidationError('The engine style name cannot be empty.')

        existing_engine_styles = self.engine_style_repository.find_by(name=name)

        if len(existing_engine_styles) > 0:
            raise ValidationError(f'An engine style with the name "{name}" already exists.')

    def validate_id(self, engine_style_id: int):
        if not engine_style_id:
            raise ValidationError('The engine style id cannot be empty.')

        engine_style = self.engine_style_repository.find_one(engine_style_id)

        if not engine_style:
            raise ValidationError(f'No engine style with the id "{engine_style_id}" exists.')
