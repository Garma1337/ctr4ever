# coding=utf-8

from typing import List

from ctr4ever.models.repository.rulesetrepository import RulesetRepository
from ctr4ever.models.ruleset import Ruleset
from ctr4ever.services.installer.installer import Installer


class RulesetInstaller(Installer):

    def __init__(self, ruleset_repository: RulesetRepository):
        self.ruleset_repository = ruleset_repository

    def _validate_entry(self, entry: dict):
        if not 'name' in entry or not entry['name']:
            raise ValueError('Ruleset name is required')

    def _parse_json(self, json_content: list[dict]) -> List[Ruleset]:
        rulesets: List[Ruleset] = []

        for entry in json_content:
            rulesets.append(Ruleset(name=entry['name']))

        return rulesets

    def _create_entries(self, rulesets: List[Ruleset]):
        for ruleset in rulesets:
            result = self.ruleset_repository.find_by(ruleset.name)

            if len(result) > 0:
                existing_ruleset = result[0]
                self.ruleset_repository.update(id=existing_ruleset.id, name=ruleset.name)
            else:
                self.ruleset_repository.create(ruleset.name)
