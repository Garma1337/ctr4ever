# coding=utf-8

from unittest import TestCase
from unittest.mock import Mock

from ctr4ever.helpers.filesystem import FileSystem
from ctr4ever.services.installer.countryinstaller import CountryInstaller
from ctr4ever.tests.mockmodelrepository import MockCountryRepository


class CountryInstallerTest(TestCase):

    def setUp(self):
        self.country_repository = MockCountryRepository()
        self.country_installer = CountryInstaller(self.country_repository)

    def test_can_install_countries(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": "USA", "flag": "us.png"}, {"name": "Japan", "flag": "jp.png"}]')

        self.country_installer.install('countries.json')
        countries = self.country_repository.find_by()

        self.assertEqual(2, len(countries))
        self.assertEqual('USA', countries[0].name)
        self.assertEqual('us.png', countries[0].flag)
        self.assertEqual('Japan', countries[1].name)
        self.assertEqual('jp.png', countries[1].flag)

    def test_can_not_install_countries_if_file_does_not_exist(self):
        FileSystem.file_exists = Mock(return_value=False)

        with self.assertRaises(ValueError):
            self.country_installer.install('countries.json')

    def test_can_not_install_countries_if_validation_fails(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": "USA"}]')

        with self.assertRaises(ValueError):
            self.country_installer.install('countries.json')

    def test_can_parse_countries(self):
        countries = self.country_installer._parse_json([
            {'name': 'USA', 'flag': 'us.png'},
            {'name': 'Japan', 'flag': 'jp.png'}
        ])

        self.assertEqual(2, len(countries))
        self.assertEqual('USA', countries[0].name)
        self.assertEqual('us.png', countries[0].flag)
        self.assertEqual('Japan', countries[1].name)
        self.assertEqual('jp.png', countries[1].flag)

    def test_can_create_countries(self):
        countries = self.country_installer._parse_json([
            {'name': 'USA', 'flag': 'us.png'},
            {'name': 'Japan', 'flag': 'jp.png'}
        ])

        self.country_installer._create_entries(countries)
        countries = self.country_repository.find_by()

        self.assertEqual(2, len(countries))
        self.assertEqual('USA', countries[0].name)
        self.assertEqual('us.png', countries[0].flag)
        self.assertEqual('Japan', countries[1].name)
        self.assertEqual('jp.png', countries[1].flag)

    def test_can_update_existing_countries(self):
        countries = self.country_installer._parse_json([
            {'name': 'USA', 'flag': 'usa.png'},
            {'name': 'Japan', 'flag': 'jpn.png'}
        ])

        self.country_installer._create_entries(countries)
        countries = self.country_repository.find_by()

        self.assertEqual(2, len(countries))
        self.assertEqual('USA', countries[0].name)
        self.assertEqual('usa.png', countries[0].flag)
        self.assertEqual('Japan', countries[1].name)
        self.assertEqual('jpn.png', countries[1].flag)

    def test_can_not_validate_country_if_name_is_missing(self):
        with self.assertRaises(ValueError):
            self.country_installer._validate_entry({'flag': 'us.png'})

    def test_can_not_validate_country_if_name_is_empty(self):
        with self.assertRaises(ValueError):
            self.country_installer._validate_entry({'name': '', 'flag': 'us.png'})

    def test_can_not_validate_country_if_flag_is_missing(self):
        with self.assertRaises(ValueError):
            self.country_installer._validate_entry({'name': 'USA'})

    def test_can_not_validate_country_if_flag_is_empty(self):
        with self.assertRaises(ValueError):
            self.country_installer._validate_entry({'name': 'USA', 'flag': ''})
