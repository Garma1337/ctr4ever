# coding=utf-8

from typing import List

from flask import Request

from ctr4ever.models.category import Category
from ctr4ever.models.repository.categoryrepository import CategoryRepository
from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response


class FindCategories(Endpoint):

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def handle_request(self, request: Request) -> Response:
        categories: List[Category] = self.category_repository.find_by(name=request.args.get('name'))

        return Response({'categories' : [category.to_dictionary() for category in categories]})

    def get_accepted_request_method(self) -> str:
        return 'GET'
