# coding=utf-8

from unittest import TestCase

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

        self.character_setup = CharacterInstaller(
            self.character_repository,
            self.engine_style_repository
        )

    def test_can_parse_characters(self):
        characters = self.character_setup._parse_characters([
            {'name': 'Fast Penta Penguin', 'icon': 'penta.png', 'engine': 'Max'},
            {'name': 'Dingodile', 'icon': 'dingo.png', 'engine': 'Speed'},
            {'name': 'Coco Bandicoot', 'icon': 'coco.png', 'engine': 'Acceleration'},
            {'name': 'Crash Bandicoot', 'icon': 'crash.png', 'engine': 'Balanced'},
            {'name': 'Polar', 'icon': 'polar.png', 'engine': 'Turning'}
        ])

        self.assertEqual(5, len(characters))
        self.assertEqual('Fast Penta Penguin', characters[0].name)
        self.assertEqual('penta.png', characters[0].icon)
        self.assertEqual(self.max_engine.id, characters[0].engine_style_id)
        self.assertEqual('Dingodile', characters[1].name)
        self.assertEqual('dingo.png', characters[1].icon)
        self.assertEqual(self.speed_engine.id, characters[1].engine_style_id)
        self.assertEqual('Coco Bandicoot', characters[2].name)
        self.assertEqual('coco.png', characters[2].icon)
        self.assertEqual(self.accel_engine.id, characters[2].engine_style_id)
        self.assertEqual('Crash Bandicoot', characters[3].name)
        self.assertEqual('crash.png', characters[3].icon)
        self.assertEqual(self.balanced_engine.id, characters[3].engine_style_id)
        self.assertEqual('Polar', characters[4].name)
        self.assertEqual('polar.png', characters[4].icon)
        self.assertEqual(self.turning_engine.id, characters[4].engine_style_id)

    def test_can_not_parse_characters_if_name_is_empty(self):
        with self.assertRaises(ValueError):
            self.character_setup._parse_characters([
                {'name': 'Penta Penguin', 'icon': 'penta.png', 'engine': 'Speed'},
                {'name': '', 'icon': 'coco.png', 'engine': 'Acceleration'}
            ])

    def test_can_not_parse_characters_if_name_is_missing(self):
        with self.assertRaises(ValueError):
            self.character_setup._parse_characters([
                {'name': 'Penta Penguin', 'icon': 'penta.png', 'engine': 'Speed'},
                {'icon': 'coco.png', 'engine': 'Acceleration'}
            ])

    def test_can_not_parse_characters_if_icon_is_empty(self):
        with self.assertRaises(ValueError):
            self.character_setup._parse_characters([
                {'name': 'Penta Penguin', 'icon': 'penta.png', 'engine': 'Speed'},
                {'name': 'Coco Bandicoot', 'icon': '', 'engine': 'Acceleration'}
            ])

    def test_can_not_parse_characters_if_icon_is_missing(self):
        with self.assertRaises(ValueError):
            self.character_setup._parse_characters([
                {'name': 'Penta Penguin', 'icon': 'penta.png', 'engine': 'Speed'},
                {'name': 'Coco Bandicoot', 'engine': 'Acceleration'}
            ])

    def test_can_not_parse_characters_if_engine_is_empty(self):
        with self.assertRaises(ValueError):
            self.character_setup._parse_characters([
                {'name': 'Penta Penguin', 'icon': 'penta.png', 'engine': 'Speed'},
                {'name': 'Coco Bandicoot', 'icon': 'coco.png', 'engine': ''}
            ])

    def test_can_not_parse_characters_if_engine_is_missing(self):
        with self.assertRaises(ValueError):
            self.character_setup._parse_characters([
                {'name': 'Penta Penguin', 'icon': 'penta.png', 'engine': 'Speed'},
                {'name': 'Coco Bandicoot', 'icon': 'coco.png'}
            ])

    def test_can_not_parse_characters_if_engine_does_not_exist(self):
        with self.assertRaises(ValueError):
            self.character_setup._parse_characters([
                {'name': 'Penta Penguin', 'icon': 'penta.png', 'engine': 'Speed'},
                {'name': 'Coco Bandicoot', 'icon': 'coco.png', 'engine': 'Unknown'}
            ])
