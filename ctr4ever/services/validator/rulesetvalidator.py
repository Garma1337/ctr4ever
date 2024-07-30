# coding=utf-8

from ctr4ever.models.repository.rulesetrepository import RulesetRepository
from ctr4ever.services.validator.validator import Validator, ValidationError


class RulesetValidator(Validator):

    def __init__(self, ruleset_repository: RulesetRepository):
        self.ruleset_repository = ruleset_repository

    def validate_ruleset(self, name: str):
        self.validate_name(name)

    def validate_name(self, name: str):
        if not name:
            raise ValidationError('The ruleset name cannot be empty.')

        existing_rulesets = self.ruleset_repository.find_by(name=name)

        if len(existing_rulesets) > 0:
            raise ValidationError(f'A ruleset with the name "{name}" already exists.')

    def validate_id(self, ruleset_id: int):
        if not ruleset_id:
            raise ValidationError('The ruleset id cannot be empty.')

        ruleset = self.ruleset_repository.find_one(ruleset_id)

        if not ruleset:
            raise ValidationError(f'No ruleset with the id "{ruleset_id}" exists.')
