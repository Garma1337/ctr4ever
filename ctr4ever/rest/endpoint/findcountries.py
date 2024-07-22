# coding=utf-8

from typing import List

from flask import Request

from ctr4ever.models.country import Country
from ctr4ever.models.repository.countryrepository import CountryRepository
from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response


class FindCountries(Endpoint):

    def __init__(self, country_repository: CountryRepository):
        self.country_repository = country_repository

    def handle_request(self, request: Request) -> Response:
        countries: List[Country] = self.country_repository.find_by(name=request.args.get('name'))

        return Response({'countries' : [character.to_dictionary() for character in countries]})

    def get_accepted_request_method(self) -> str:
        return 'GET'

    def require_authentication(self) -> bool:
        return False
