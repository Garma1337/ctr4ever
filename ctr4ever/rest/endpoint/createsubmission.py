# coding=utf-8

from flask import Request

from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import ErrorResponse, Response
from ctr4ever.services.submissionmanager import SubmissionManager
from ctr4ever.services.timeformatter import TimeFormatter


class CreateSubmission(Endpoint):

    def __init__(self, submission_manager: SubmissionManager, time_formatter: TimeFormatter):
        self.submission_manager = submission_manager
        self.time_formatter = time_formatter

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

        submission = self.submission_manager.submit_time(
            int(current_user['id']),
            int(track_id),
            int(category_id),
            int(character_id),
            int(game_version_id),
            int(ruleset_id),
            int(platform_id),
            parsed_time.in_seconds(),
            video
        )

        return Response({'submission': submission.to_dictionary()})

    def get_accepted_request_method(self):
        return 'POST'

    def require_authentication(self):
        return True
