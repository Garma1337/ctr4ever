# coding=utf-8

from unittest import TestCase

from ctr4ever.services.installer.categoryinstaller import CategoryInstaller
from ctr4ever.tests.mockmodelrepository import MockCategoryRepository


class CategoryInstallerTest(TestCase):

    def setUp(self):
        self.category_repository = MockCategoryRepository()
        self.category_setup = CategoryInstaller(self.category_repository)

    def test_can_parse_categories(self):
        categories = self.category_setup._parse_categories([
            {'name': 'category1'},
            {'name': 'category2'}
        ])

        self.assertEqual(2, len(categories))
        self.assertEqual('category1', categories[0].name)
        self.assertEqual('category2', categories[1].name)

    def test_can_not_parse_categories_if_name_is_empty(self):
        with self.assertRaises(ValueError):
            self.category_setup._parse_categories([
                {'name': 'category1'},
                {'name': ''}
            ])

    def test_can_not_parse_categories_if_name_is_missing(self):
        with self.assertRaises(ValueError):
            self.category_setup._parse_categories([
                {'name': 'category1'},
                {}
            ])
