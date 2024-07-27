# coding=utf-8

from flask import Request

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import ErrorResponse, SuccessResponse
from ctr4ever.services.submissionmanager import SubmissionManager, SubmissionError
from ctr4ever.services.timeformatter import TimeFormatter


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

        if not track_id:
            return ErrorResponse('A track is required.')

        if not category_id:
            return ErrorResponse('A category is required.')

        if not character_id:
            return ErrorResponse('A character is required.')

        if not game_version_id:
            return ErrorResponse('A game version is required.')

        if not ruleset_id:
            return ErrorResponse('A ruleset is required.')

        if not platform_id:
            return ErrorResponse('A platform is required.')

        if not time:
            return ErrorResponse('A time is required.')

        if not video:
            return ErrorResponse('A video is required.')

        parsed_time = self.time_formatter.create_time_from_format(time)

        if not parsed_time:
            return ErrorResponse('Invalid time format.')

        if self.max_comment_length:
            if comment and len(comment) > self.max_comment_length:
                return ErrorResponse('The comment is too long.')

        try:
            submission = self.submission_manager.submit_time(
                int(current_user['id']),
                int(track_id),
                int(category_id),
                int(character_id),
                int(game_version_id),
                int(ruleset_id),
                int(platform_id),
                parsed_time.in_seconds(),
                video,
                comment
            )
        except SubmissionError as e:
            return ErrorResponse(str(e))

        return SuccessResponse({'submission': submission.to_dictionary()})

    def get_accepted_request_method(self):
        return 'POST'

    def require_authentication(self):
        return True
