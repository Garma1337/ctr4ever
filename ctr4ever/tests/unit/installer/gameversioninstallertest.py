# coding=utf-8

from unittest import TestCase
from unittest.mock import Mock

from ctr4ever.helpers.filesystem import FileSystem
from ctr4ever.models.gameversion import GameVersion
from ctr4ever.services.installer.gameversioninstaller import GameVersionInstaller
from ctr4ever.tests.mockmodelrepository import MockGameVersionRepository


class GameVersionInstallerTest(TestCase):

    def setUp(self):
        self.game_version_repository = MockGameVersionRepository()
        self.game_version_installer = GameVersionInstaller(self.game_version_repository)

    def test_can_install_game_versions(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": "PAL", "icon": "pal.png"}, {"name": "NTSC-J", "icon": "ntscj.png"}]')

        self.game_version_installer.install('game_versions.json')
        game_versions = self.game_version_repository.find_by()

        self.assertEqual(2, len(game_versions))
        self.assertEqual('PAL', game_versions[0].name)
        self.assertEqual('pal.png', game_versions[0].icon)
        self.assertEqual('NTSC-J', game_versions[1].name)
        self.assertEqual('ntscj.png', game_versions[1].icon)

    def test_can_not_install_game_versions_if_file_does_not_exist(self):
        FileSystem.file_exists = Mock(return_value=False)

        with self.assertRaises(ValueError):
            self.game_version_installer.install('game_versions.json')

    def test_can_not_install_game_versions_if_validation_fails(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": ""}]')

        with self.assertRaises(ValueError):
            self.game_version_installer.install('game_versions.json')

    def test_can_create_game_versions(self):
        self.game_version_installer._upsert_game_versions([
            GameVersion(name='PAL', icon='pal.png'),
            GameVersion(name='NTSC-J', icon='ntscj.png')
        ])

        game_versions = self.game_version_repository.find_by()

        self.assertEqual(2, len(game_versions))
        self.assertEqual('PAL', game_versions[0].name)
        self.assertEqual('pal.png', game_versions[0].icon)
        self.assertEqual('NTSC-J', game_versions[1].name)
        self.assertEqual('ntscj.png', game_versions[1].icon)

    def test_can_update_existing_game_versions(self):
        self.game_version_repository.create('PAL', 'pal.png')
        self.game_version_repository.create('NTSC-J', 'ntscj.png')

        self.game_version_installer._upsert_game_versions([
            GameVersion(name='PAL', icon='pal2.png'),
            GameVersion(name='NTSC-J', icon='ntscj2.png')
        ])

        game_versions = self.game_version_repository.find_by()

        self.assertEqual(2, len(game_versions))
        self.assertEqual('PAL', game_versions[0].name)
        self.assertEqual('pal2.png', game_versions[0].icon)
        self.assertEqual('NTSC-J', game_versions[1].name)
        self.assertEqual('ntscj2.png', game_versions[1].icon)

    def test_can_parse_game_versions(self):
        game_versions = self.game_version_installer._parse_game_versions([
            {'name': 'PAL', 'icon': 'pal.png'},
            {'name': 'NTSC-J', 'icon': 'ntscj.png'}
        ])

        self.assertEqual(2, len(game_versions))
        self.assertEqual('PAL', game_versions[0].name)
        self.assertEqual('pal.png', game_versions[0].icon)
        self.assertEqual('NTSC-J', game_versions[1].name)
        self.assertEqual('ntscj.png', game_versions[1].icon)

    def test_can_not_validate_game_version_if_name_is_missing(self):
        with self.assertRaises(ValueError):
            self.game_version_installer._validate_entry({})

    def test_can_not_validate_game_version_if_name_is_empty(self):
        with self.assertRaises(ValueError):
            self.game_version_installer._validate_entry({'name': ''})

    def test_can_not_validate_game_version_if_icon_is_missing(self):
        with self.assertRaises(ValueError):
            self.game_version_installer._validate_entry({'name': 'PAL'})

    def test_can_not_validate_game_version_if_icon_is_empty(self):
        with self.assertRaises(ValueError):
            self.game_version_installer._validate_entry({'name': 'PAL', 'icon': ''})
