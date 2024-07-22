# coding=utf-8

from typing import List

from flask import Request

from ctr4ever.helpers.pagination import Pagination
from ctr4ever.models.repository.submissionrepository import SubmissionRepository
from ctr4ever.models.submission import Submission
from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response


class FindSubmissions(Endpoint):

    def __init__(self, submission_repository: SubmissionRepository):
        self.submission_repository = submission_repository

    def handle_request(self, request: Request) -> Response:
        player_count = self.submission_repository.count(
            player_id=request.args.get('player_id'),
            track_id=request.args.get('track_id'),
            category_id=request.args.get('category_id'),
            character_id=request.args.get('character_id'),
            game_version_id=request.args.get('game_version_id'),
            ruleset_id=request.args.get('ruleset_id'),
            platform_id=request.args.get('platform_id')
        )

        pagination = Pagination(request.args.get('page', 1), request.args.get('per_page', 20), player_count)

        submissions: List[Submission] = self.submission_repository.find_by(
            player_id=request.args.get('player_id'),
            track_id=request.args.get('track_id'),
            category_id=request.args.get('category_id'),
            character_id=request.args.get('character_id'),
            game_version_id=request.args.get('game_version_id'),
            ruleset_id=request.args.get('ruleset_id'),
            platform_id=request.args.get('platform_id'),
            limit=pagination.get_limit(),
            offset=pagination.get_offset()
        )

        return Response({'pagination': pagination.to_dictionary(), 'submissions' : [submission.to_dictionary() for submission in submissions]})

    def get_accepted_request_method(self) -> str:
        return 'GET'

    def require_authentication(self) -> bool:
        return False
