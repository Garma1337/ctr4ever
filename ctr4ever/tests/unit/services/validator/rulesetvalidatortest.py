# coding=utf-8

from unittest import TestCase

from ctr4ever.services.validator.rulesetvalidator import RulesetValidator
from ctr4ever.services.validator.validator import ValidationError
from ctr4ever.tests.mockmodelrepository import MockRulesetRepository


class RulesetValidatorTest(TestCase):

    def setUp(self):
        self.ruleset_repository = MockRulesetRepository()
        self.ruleset_validator = RulesetValidator(self.ruleset_repository)

    def test_can_validate_ruleset_name(self):
        self.ruleset_validator.validate_name('Classic')

    def test_can_not_validate_empty_ruleset_name(self):
        with self.assertRaises(ValidationError):
            self.ruleset_validator.validate_name('')

    def test_can_not_validate_existing_ruleset_name(self):
        self.ruleset_repository.create('Classic')

        with self.assertRaises(ValidationError):
            self.ruleset_validator.validate_name('Classic')

    def test_can_validate_ruleset_id(self):
        ruleset = self.ruleset_repository.create('Classic')

        self.ruleset_validator.validate_id(ruleset.id)

    def test_can_not_validate_empty_ruleset_id(self):
        with self.assertRaises(ValidationError):
            self.ruleset_validator.validate_id(None)

    def test_can_not_validate_nonexistent_ruleset_id(self):
        with self.assertRaises(ValidationError):
            self.ruleset_validator.validate_id(1)
