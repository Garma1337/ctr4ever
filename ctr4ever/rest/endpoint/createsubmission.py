# coding=utf-8

from flask import Request

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import ErrorResponse, SuccessResponse
from ctr4ever.services.submissionmanager import SubmissionManager, SubmissionError
from ctr4ever.services.timeformatter import TimeFormatter
from ctr4ever.services.validator.validator import ValidationError


class CreateSubmission(Endpoint):

    def __init__(self, submission_manager: SubmissionManager, time_formatter: TimeFormatter, max_comment_length: int):
        self.submission_manager = submission_manager
        self.time_formatter = time_formatter
        self.max_comment_length = max_comment_length

    def handle_request(self, request: Request):
        current_user = self._get_current_user()

        track_id = request.json.get('track_id')
        category_id = request.json.get('category_id')
        character_id = request.json.get('character_id')
        game_version_id = request.json.get('game_version_id')
        ruleset_id = request.json.get('ruleset_id')
        platform_id = request.json.get('platform_id')
        time = request.json.get('time')
        video = request.json.get('video')
        comment = request.json.get('comment')

        try:
            submission = self.submission_manager.submit_time(
                int(current_user['id']),
                int(track_id),
                int(category_id),
                int(character_id),
                int(game_version_id),
                int(ruleset_id),
                int(platform_id),
                time,
                video,
                comment
            )
        except ValidationError as e:
            return ErrorResponse(str(e))

        return SuccessResponse({'submission': submission.to_dictionary()})

    def get_accepted_request_method(self):
        return 'POST'

    def require_authentication(self):
        return True
