# coding=utf-8

from ctr4ever.models.repository.platformrepository import PlatformRepository
from ctr4ever.services.validator.validator import Validator, ValidationError


class PlatformValidator(Validator):

    def __init__(self, platform_repository: PlatformRepository):
        self.platform_repository = platform_repository

    def validate_platform(self, name: str):
        self.validate_name(name)

    def validate_name(self, name: str):
        if not name:
            raise ValidationError('The platform name cannot be empty.')

        existing_platforms = self.platform_repository.find_by(name=name)

        if len(existing_platforms) > 0:
            raise ValidationError(f'A platform with the name "{name}" already exists.')

    def validate_id(self, platform_id: int):
        if not platform_id:
            raise ValidationError('The platform id cannot be empty.')

        platform = self.platform_repository.find_one(platform_id)

        if not platform:
            raise ValidationError(f'No platform with the id "{platform_id}" exists.')
