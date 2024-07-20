# coding=utf-8

from unittest import TestCase
from unittest.mock import Mock

from ctr4ever.helpers.filesystem import FileSystem
from ctr4ever.models.ruleset import Ruleset
from ctr4ever.services.installer.rulesetinstaller import RulesetInstaller
from ctr4ever.tests.mockmodelrepository import MockRulesetRepository


class RulesetInstallerTest(TestCase):

    def setUp(self):
        self.ruleset_repository = MockRulesetRepository()
        self.ruleset_installer = RulesetInstaller(self.ruleset_repository)

    def test_can_install_ruleset(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": "Unrestricted"}, {"name": "Classic"}]')

        self.ruleset_installer.install('rulesets.json')
        rulesets = self.ruleset_repository.find_by()

        self.assertEqual(2, len(rulesets))
        self.assertEqual('Unrestricted', rulesets[0].name)
        self.assertEqual('Classic', rulesets[1].name)

    def test_can_not_install_ruleset_if_file_does_not_exist(self):
        FileSystem.file_exists = Mock(return_value=False)

        with self.assertRaises(ValueError):
            self.ruleset_installer.install('rulesets.json')

    def test_can_not_install_ruleset_if_validation_fails(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": ""}]')

        with self.assertRaises(ValueError):
            self.ruleset_installer.install('rulesets.json')

    def test_can_create_ruleset(self):
        self.ruleset_installer._create_entries([
            Ruleset(name='Unrestricted'),
            Ruleset(name='Classic')
        ])

        rulesets = self.ruleset_repository.find_by()
        self.assertEqual(2, len(rulesets))
        self.assertEqual('Unrestricted', rulesets[0].name)
        self.assertEqual('Classic', rulesets[1].name)

    def test_can_update_existing_ruleset(self):
        self.ruleset_repository.create('Unrestricted')
        self.ruleset_repository.create('Classic')

        self.ruleset_installer._create_entries([
            Ruleset(name='Unrestricted'),
            Ruleset(name='Classic')
       ])

        rulesets = self.ruleset_repository.find_by()
        self.assertEqual(2, len(rulesets))
        self.assertEqual('Unrestricted', rulesets[0].name)
        self.assertEqual('Classic', rulesets[1].name)

    def test_can_parse_ruleset(self):
        rulesets = self.ruleset_installer._parse_json([
            {"name": "Classic"}
        ])

        self.assertEqual(1, len(rulesets))
        self.assertEqual('Classic', rulesets[0].name)

    def test_can_not_validate_ruleset_if_name_is_missing(self):
        with self.assertRaises(ValueError):
            self.ruleset_installer._validate_entry({})

    def test_can_not_validate_ruleset_if_name_is_empty(self):
        with self.assertRaises(ValueError):
            self.ruleset_installer._validate_entry({'name': ''})
