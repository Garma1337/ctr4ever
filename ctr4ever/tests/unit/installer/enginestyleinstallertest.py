# coding=utf-8

from unittest import TestCase
from unittest.mock import Mock

from ctr4ever.helpers.filesystem import FileSystem
from ctr4ever.models.enginestyle import EngineStyle
from ctr4ever.services.installer.enginestyleinstaller import EngineStyleInstaller
from ctr4ever.tests.mockmodelrepository import MockEngineStyleRepository


class EngineStyleInstallerTest(TestCase):

    def setUp(self):
        self.engine_style_repository = MockEngineStyleRepository()
        self.engine_style_installer = EngineStyleInstaller(self.engine_style_repository)

    def test_can_install_engine_styles(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": "Max"}, {"name": "Speed"}, {"name": "Acceleration"}, {"name": "Balanced"}, {"name": "Turning"}]')

        self.engine_style_installer.install('engine_styles.json')
        engine_styles = self.engine_style_repository.find_by()

        self.assertEqual(5, len(engine_styles))
        self.assertEqual('Max', engine_styles[0].name)
        self.assertEqual('Speed', engine_styles[1].name)
        self.assertEqual('Acceleration', engine_styles[2].name)
        self.assertEqual('Balanced', engine_styles[3].name)
        self.assertEqual('Turning', engine_styles[4].name)

    def test_can_not_install_engine_styles_if_file_does_not_exist(self):
        FileSystem.file_exists = Mock(return_value=False)

        with self.assertRaises(ValueError):
            self.engine_style_installer.install('engine_styles.json')

    def test_can_not_install_engine_styles_if_validation_fails(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": ""}]')

        with self.assertRaises(ValueError):
            self.engine_style_installer.install('engine_styles.json')

    def test_can_create_engine_styles(self):
        self.engine_style_installer._upsert_engine_styles([
            EngineStyle(name='Max'),
            EngineStyle(name='Speed'),
            EngineStyle(name='Acceleration'),
            EngineStyle(name='Balanced'),
            EngineStyle(name='Turning')
        ])

        engine_styles = self.engine_style_repository.find_by()

        self.assertEqual(5, len(engine_styles))
        self.assertEqual('Max', engine_styles[0].name)
        self.assertEqual('Speed', engine_styles[1].name)
        self.assertEqual('Acceleration', engine_styles[2].name)
        self.assertEqual('Balanced', engine_styles[3].name)
        self.assertEqual('Turning', engine_styles[4].name)

    def test_can_update_existing_engine_styles(self):
        self.engine_style_repository.create('Max')
        self.engine_style_repository.create('Speed')
        self.engine_style_repository.create('Acceleration')
        self.engine_style_repository.create('Balanced')
        self.engine_style_repository.create('Turning')

        self.engine_style_installer._upsert_engine_styles([
            EngineStyle(name='Max'),
            EngineStyle(name='Speed'),
            EngineStyle(name='Acceleration'),
            EngineStyle(name='Balanced'),
            EngineStyle(name='Turning')
        ])

        engine_styles = self.engine_style_repository.find_by()

        self.assertEqual(5, len(engine_styles))
        self.assertEqual('Max', engine_styles[0].name)
        self.assertEqual('Speed', engine_styles[1].name)
        self.assertEqual('Acceleration', engine_styles[2].name)
        self.assertEqual('Balanced', engine_styles[3].name)
        self.assertEqual('Turning', engine_styles[4].name)

    def test_can_parse_engine_styles(self):
        engine_styles = self.engine_style_installer._parse_engine_styles([
            {'name': 'Max'},
            {'name': 'Speed'},
            {'name': 'Acceleration'},
            {'name': 'Balanced'},
            {'name': 'Turning'}
        ])

        self.assertEqual(5, len(engine_styles))
        self.assertEqual('Max', engine_styles[0].name)
        self.assertEqual('Speed', engine_styles[1].name)
        self.assertEqual('Acceleration', engine_styles[2].name)
        self.assertEqual('Balanced', engine_styles[3].name)
        self.assertEqual('Turning', engine_styles[4].name)

    def test_can_not_validate_engine_style_if_name_is_missing(self):
        with self.assertRaises(ValueError):
            self.engine_style_installer._validate_entry({})

    def test_can_not_validate_engine_style_if_name_is_empty(self):
        with self.assertRaises(ValueError):
            self.engine_style_installer._validate_entry({'name': ''})
