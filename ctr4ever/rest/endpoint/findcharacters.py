# coding=utf-8

from typing import List

from flask import Request

from ctr4ever.models.character import Character
from ctr4ever.models.repository.characterrepository import CharacterRepository
from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response


class FindCharacters(Endpoint):

    def __init__(self, character_repository: CharacterRepository):
        self.character_repository = character_repository

    def handle_request(self, request: Request) -> Response:
        characters: List[Character] = self.character_repository.find_by(name=request.args.get('name'))

        return Response({'characters' : [character.to_dictionary() for character in characters]})

    def get_accepted_request_method(self) -> str:
        return 'GET'
