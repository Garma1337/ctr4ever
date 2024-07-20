# coding=utf-8

from unittest import TestCase
from unittest.mock import Mock

from ctr4ever.helpers.filesystem import FileSystem
from ctr4ever.models.platform import Platform
from ctr4ever.services.installer.platforminstaller import PlatformInstaller
from ctr4ever.tests.mockmodelrepository import MockPlatformRepository


class PlatformInstallerTest(TestCase):

    def setUp(self):
        self.platform_repository = MockPlatformRepository()
        self.platform_installer = PlatformInstaller(self.platform_repository)

    def test_can_install_platforms(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": "PAL"}, {"name": "NSTC-J"}]')

        self.platform_installer.install('platforms.json')
        platforms = self.platform_repository.find_by()

        self.assertEqual(2, len(platforms))
        self.assertEqual('PAL', platforms[0].name)
        self.assertEqual('NSTC-J', platforms[1].name)

    def test_can_not_install_platforms_if_file_does_not_exist(self):
        FileSystem.file_exists = Mock(return_value=False)

        with self.assertRaises(ValueError):
            self.platform_installer.install('platforms.json')

    def test_can_not_install_platforms_if_validation_fails(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": ""}]')

        with self.assertRaises(ValueError):
            self.platform_installer.install('platforms.json')

    def test_can_create_platforms(self):
        self.platform_installer._create_entries([
            Platform(name='PAL'),
            Platform(name='NSTC-J')
        ])

        platforms = self.platform_repository.find_by()
        self.assertEqual(2, len(platforms))
        self.assertEqual('PAL', platforms[0].name)
        self.assertEqual('NSTC-J', platforms[1].name)

    def test_can_update_existing_platforms(self):
        self.platform_repository.create('PAL')
        self.platform_repository.create('NSTC-J')

        self.platform_installer._create_entries([
            Platform(name='PAL'),
            Platform(name='NSTC-J')
        ])

        platforms = self.platform_repository.find_by()
        self.assertEqual(2, len(platforms))
        self.assertEqual('PAL', platforms[0].name)
        self.assertEqual('NSTC-J', platforms[1].name)

    def test_can_parse_platforms(self):
        platforms = self.platform_installer._parse_json([
            {'name': 'PAL'},
            {'name': 'NSTC-J'}
        ])

        self.assertEqual(2, len(platforms))
        self.assertEqual('PAL', platforms[0].name)
        self.assertEqual('NSTC-J', platforms[1].name)

    def test_can_not_validate_platform_if_name_is_missing(self):
        with self.assertRaises(ValueError):
            self.platform_installer._validate_entry({})

    def test_can_not_validate_platform_if_name_is_empty(self):
        with self.assertRaises(ValueError):
            self.platform_installer._validate_entry({'name': ''})
