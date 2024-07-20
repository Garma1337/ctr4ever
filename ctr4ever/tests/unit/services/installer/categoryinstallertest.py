# coding=utf-8

from unittest import TestCase
from unittest.mock import Mock

from ctr4ever.helpers.filesystem import FileSystem
from ctr4ever.models.category import Category
from ctr4ever.services.installer.categoryinstaller import CategoryInstaller
from ctr4ever.tests.mockmodelrepository import MockCategoryRepository


class CategoryInstallerTest(TestCase):

    def setUp(self):
        self.category_repository = MockCategoryRepository()
        self.category_installer = CategoryInstaller(self.category_repository)

    def test_can_install_categories(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": "category1"}, {"name": "category2"}]')

        self.category_installer.install('categories.json')
        categories = self.category_repository.find_by()

        self.assertEqual(2, len(categories))
        self.assertEqual('category1', categories[0].name)
        self.assertEqual('category2', categories[1].name)

    def test_can_not_install_categories_if_file_does_not_exist(self):
        FileSystem.file_exists = Mock(return_value=False)

        with self.assertRaises(ValueError):
            self.category_installer.install('categories.json')

    def test_can_not_install_categories_if_validation_fails(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": ""}]')

        with self.assertRaises(ValueError):
            self.category_installer.install('categories.json')

    def test_can_create_categories(self):
        self.category_installer._create_entries([
            Category(name='category1'),
            Category(name='category2')
        ])

        categories = self.category_repository.find_by()
        self.assertEqual(2, len(categories))
        self.assertEqual('category1', categories[0].name)
        self.assertEqual('category2', categories[1].name)

    def test_can_update_existing_categories(self):
        self.category_repository.create('category1')
        self.category_repository.create('category2')

        self.category_installer._create_entries([
            Category(name='category1'),
            Category(name='category2')
        ])

        categories = self.category_repository.find_by()
        self.assertEqual(2, len(categories))
        self.assertEqual('category1', categories[0].name)
        self.assertEqual('category2', categories[1].name)

    def test_can_parse_categories(self):
        categories = self.category_installer._parse_json([
            {'name': 'category1'},
            {'name': 'category2'}
        ])

        self.assertEqual(2, len(categories))
        self.assertEqual('category1', categories[0].name)
        self.assertEqual('category2', categories[1].name)

    def test_can_not_validate_category_if_name_is_missing(self):
        with self.assertRaises(ValueError):
            self.category_installer._validate_entry({})

    def test_can_not_validate_category_if_name_is_empty(self):
        with self.assertRaises(ValueError):
            self.category_installer._validate_entry({'name': ''})
