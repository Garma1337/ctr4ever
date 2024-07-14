# coding=utf-8

import math

from marshmallow import Schema, fields


class PaginationSchema(Schema):
    current_page = fields.Int()
    items_per_page = fields.Int()
    total_item_count = fields.Int()


class Pagination(object):

    def __init__(self, current_page: int, items_per_page: int, total_item_count: int):
        self.current_page = int(current_page)
        self.items_per_page = int(items_per_page)
        self.total_item_count = int(total_item_count)

        if self.current_page < 1:
            raise ValueError('The current page must be greater than 0')

        if self.items_per_page < 1:
            raise ValueError('The number of items per page must be greater than 0')

    def get_page(self) -> int:
        return self.current_page

    def get_page_size(self) -> int:
        return self.items_per_page

    def get_offset(self) -> int:
        return (self.current_page - 1) * self.items_per_page

    def get_limit(self) -> int:
        return self.items_per_page

    def get_item_count(self) -> int:
        return self.total_item_count

    def get_page_count(self) -> int:
        return math.ceil(self.total_item_count / self.items_per_page) or 1

    def get_next_page(self) -> int:
        return self.current_page + 1 if self.current_page < self.get_page_count() else self.current_page

    def get_previous_page(self) -> int:
        return self.current_page - 1 if self.current_page > 1 else self.current_page

    def has_next_page(self) -> bool:
        return self.current_page < self.get_page_count()

    def has_previous_page(self) -> bool:
        return self.current_page > 1

    def to_dictionary(self) -> dict:
        return PaginationSchema().dump(self)
