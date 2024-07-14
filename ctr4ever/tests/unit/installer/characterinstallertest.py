# coding=utf-8

from unittest import TestCase
from unittest.mock import Mock

from ctr4ever.helpers.filesystem import FileSystem
from ctr4ever.models.character import Character
from ctr4ever.services.installer.characterinstaller import CharacterInstaller
from ctr4ever.tests.mockmodelrepository import MockCharacterRepository, MockEngineStyleRepository


class CharacterInstallerTest(TestCase):

    def setUp(self):
        self.character_repository = MockCharacterRepository()
        self.engine_style_repository = MockEngineStyleRepository()

        self.max_engine = self.engine_style_repository.create('Max')
        self.speed_engine = self.engine_style_repository.create('Speed')
        self.accel_engine = self.engine_style_repository.create('Acceleration')
        self.balanced_engine = self.engine_style_repository.create('Balanced')
        self.turning_engine = self.engine_style_repository.create('Turning')

        self.character_installer = CharacterInstaller(
            self.character_repository,
            self.engine_style_repository
        )

    def test_can_install_characters(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": "Penta Penguin", "icon": "penta.png", "engine": "Max"}, {"name": "Dingodile", "icon": "dingo.png", "engine": "Speed"}]')

        self.character_installer.install('characters.json')
        characters = self.character_repository.find_by()

        self.assertEqual(2, len(characters))
        self.assertEqual('Penta Penguin', characters[0].name)
        self.assertEqual('penta.png', characters[0].icon)
        self.assertEqual(self.max_engine.id, characters[0].engine_style_id)
        self.assertEqual('Dingodile', characters[1].name)
        self.assertEqual('dingo.png', characters[1].icon)
        self.assertEqual(self.speed_engine.id, characters[1].engine_style_id)

    def test_can_not_install_characters_if_file_does_not_exist(self):
        FileSystem.file_exists = Mock(return_value=False)

        with self.assertRaises(ValueError):
            self.character_installer.install('characters.json')

    def test_can_not_install_characters_if_validation_fails(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": "Penta Penguin", "icon": "penta.png", "engine": "Unknown"}]')

        with self.assertRaises(ValueError):
            self.character_installer.install('characters.json')

    def test_can_parse_characters(self):
        characters = self.character_installer._parse_characters([
            {'name': 'Penta Penguin', 'icon': 'penta.png', 'engine': 'Max'},
            {'name': 'Dingodile', 'icon': 'dingo.png', 'engine': 'Speed'}
        ])

        self.assertEqual(2, len(characters))
        self.assertEqual('Penta Penguin', characters[0].name)
        self.assertEqual('penta.png', characters[0].icon)
        self.assertEqual(self.max_engine.id, characters[0].engine_style_id)
        self.assertEqual('Dingodile', characters[1].name)
        self.assertEqual('dingo.png', characters[1].icon)
        self.assertEqual(self.speed_engine.id, characters[1].engine_style_id)

    def test_can_create_characters(self):
        self.character_installer._upsert_characters([
            Character(name='Penta Penguin', icon='penta.png', engine_style_id=self.max_engine.id),
            Character(name='Dingodile', icon='dingo.png', engine_style_id=self.speed_engine.id)
        ])

        characters = self.character_repository.find_by()

        self.assertEqual(2, len(characters))
        self.assertEqual('Penta Penguin', characters[0].name)
        self.assertEqual('penta.png', characters[0].icon)
        self.assertEqual(self.max_engine.id, characters[0].engine_style_id)
        self.assertEqual('Dingodile', characters[1].name)
        self.assertEqual('dingo.png', characters[1].icon)
        self.assertEqual(self.speed_engine.id, characters[1].engine_style_id)

    def test_can_update_existing_characters(self):
        self.character_repository.create('Penta Penguin', self.max_engine.id, 'penta.png')
        self.character_repository.create('Dingodile', self.speed_engine.id, 'dingo.png')

        self.character_installer._upsert_characters([
            Character(name='Penta Penguin', icon='penta2.png', engine_style_id=self.speed_engine.id),
            Character(name='Dingodile', icon='dingo2.png', engine_style_id=self.accel_engine.id)
        ])

        characters = self.character_repository.find_by()

        self.assertEqual(2, len(characters))
        self.assertEqual('Penta Penguin', characters[0].name)
        self.assertEqual('penta2.png', characters[0].icon)
        self.assertEqual(self.speed_engine.id, characters[0].engine_style_id)
        self.assertEqual('Dingodile', characters[1].name)
        self.assertEqual('dingo2.png', characters[1].icon)
        self.assertEqual(self.accel_engine.id, characters[1].engine_style_id)

    def test_can_not_validate_character_if_name_is_missing(self):
        with self.assertRaises(ValueError):
            self.character_installer._validate_entry({})

    def test_can_not_validate_character_if_name_is_empty(self):
        with self.assertRaises(ValueError):
            self.character_installer._validate_entry({'name': ''})

    def test_can_not_validate_character_if_icon_is_missing(self):
        with self.assertRaises(ValueError):
            self.character_installer._validate_entry({'name': 'Penta Penguin'})

    def test_can_not_validate_character_if_icon_is_empty(self):
        with self.assertRaises(ValueError):
            self.character_installer._validate_entry({'name': 'Penta Penguin', 'icon': ''})

    def test_can_not_validate_character_if_engine_is_missing(self):
        with self.assertRaises(ValueError):
            self.character_installer._validate_entry({'name': 'Penta Penguin', 'icon': 'penta.png'})

    def test_can_not_validate_character_if_engine_is_empty(self):
        with self.assertRaises(ValueError):
            self.character_installer._validate_entry({'name': 'Penta Penguin', 'icon': 'penta.png', 'engine': ''})

    def test_can_not_validate_character_if_engine_does_not_exist(self):
        with self.assertRaises(ValueError):
            self.character_installer._validate_entry({'name': 'Penta Penguin', 'icon': 'penta.png', 'engine': 'Unknown'})
