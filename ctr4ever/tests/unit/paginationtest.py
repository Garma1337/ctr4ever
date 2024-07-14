# coding=utf-8

from unittest import TestCase

from ctr4ever.helpers.pagination import Pagination


class PaginationTest(TestCase):

    def test_can_create_pagination(self):
        pagination = Pagination(1, 5, 100)

        self.assertEqual(1, pagination.get_page())
        self.assertEqual(5, pagination.get_page_size())
        self.assertEqual(100, pagination.get_item_count())

    def test_can_calculate_offset(self):
        pagination = Pagination(2, 5, 100)

        self.assertEqual(5, pagination.get_offset())

    def test_can_calculate_limit(self):
        pagination = Pagination(2, 5, 100)

        self.assertEqual(5, pagination.get_limit())

    def test_can_calculate_page_count(self):
        pagination = Pagination(2, 5, 100)

        self.assertEqual(20, pagination.get_page_count())

    def test_can_calculate_page_count_with_remainder(self):
        pagination = Pagination(2, 5, 101)

        self.assertEqual(21, pagination.get_page_count())

    def test_can_calculate_page_count_with_no_items(self):
        pagination = Pagination(2, 5, 0)

        self.assertEqual(1, pagination.get_page_count())

    def test_can_calculate_next_page(self):
        pagination = Pagination(2, 5, 100)

        self.assertEqual(3, pagination.get_next_page())

    def test_can_calculate_next_page_at_end(self):
        pagination = Pagination(20, 5, 100)

        self.assertEqual(20, pagination.get_next_page())

    def test_can_calculate_previous_page(self):
        pagination = Pagination(2, 5, 100)

        self.assertEqual(1, pagination.get_previous_page())

    def test_can_calculate_previous_page_at_start(self):
        pagination = Pagination(1, 5, 100)

        self.assertEqual(1, pagination.get_previous_page())

    def test_cannot_create_pagination_with_invalid_current_page(self):
        with self.assertRaises(ValueError):
            Pagination(0, 5, 100)

    def test_cannot_create_pagination_with_invalid_items_per_page(self):
        with self.assertRaises(ValueError):
            Pagination(1, 0, 100)
