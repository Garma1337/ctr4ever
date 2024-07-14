# coding=utf-8

from typing import List

from flask import Request

from ctr4ever.models.repository.rulesetrepository import RulesetRepository
from ctr4ever.models.ruleset import Ruleset
from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response


class FindRulesets(Endpoint):

    def handle_request(self, request: Request) -> Response:
        ruleset_repository: RulesetRepository = self.container.get('repository.ruleset')
        rulesets: List[Ruleset] = ruleset_repository.find_by(name=request.args.get('name'))

        return Response({'rulesets' : [ruleset.to_dictionary() for ruleset in rulesets]})

    def get_accepted_request_method(self) -> str:
        return 'GET'
