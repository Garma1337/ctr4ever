# coding=utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from flask import Request

from ctr4ever.rest.endpoint.createsubmission import CreateSubmission
from ctr4ever.services.submissionmanager import SubmissionManager
from ctr4ever.services.timeformatter import TimeFormatter
from ctr4ever.tests.mockmodelrepository import MockCategoryRepository, MockCharacterRepository, \
    MockEngineStyleRepository, MockGameVersionRepository, MockPlatformRepository, MockPlayerRepository, \
    MockRulesetRepository, MockSubmissionRepository, MockTrackRepository, MockCountryRepository


class CreateSubmissionTest(TestCase):

    def setUp(self):
        self.country_repository = MockCountryRepository()
        self.category_repository = MockCategoryRepository()
        self.character_repository = MockCharacterRepository()
        self.engine_style_repository = MockEngineStyleRepository()
        self.game_version_repository = MockGameVersionRepository()
        self.platform_repository = MockPlatformRepository()
        self.player_repository = MockPlayerRepository()
        self.ruleset_repository = MockRulesetRepository()
        self.submission_repository = MockSubmissionRepository()
        self.track_repository = MockTrackRepository()

        self.germany = self.country_repository.create('Germany', 'de.png')
        self.course = self.category_repository.create('Course')
        self.speed_engine = self.engine_style_repository.create('Speed')
        self.pal = self.game_version_repository.create('PAL', 'pal.png')
        self.dingodile = self.character_repository.create('Dingodile', self.speed_engine.id, 'dingo.png')
        self.console = self.platform_repository.create('Console')
        self.classic = self.ruleset_repository.create('Classic')
        self.crash_cove = self.track_repository.create('Crash Cove')

        self.garma = self.player_repository.create(
            self.germany.id,
            'Garma',
            'test@test.com',
            '123456',
            '123456',
            True,
            datetime.now()
        )

        self.submission_manager = SubmissionManager(
            self.category_repository,
            self.character_repository,
            self.game_version_repository,
            self.platform_repository,
            self.player_repository,
            self.ruleset_repository,
            self.submission_repository,
            self.track_repository
        )

        self.time_formatter = TimeFormatter()
        self.create_submission_endpoint = CreateSubmission(self.submission_manager, self.time_formatter)

        self.create_submission_endpoint._get_current_user = Mock(return_value=self.garma.to_dictionary())

    def test_can_create_submission(self):
        request = Request.from_values(json={
            'track_id': self.crash_cove.id,
            'category_id': self.course.id,
            'character_id': self.dingodile.id,
            'game_version_id': self.pal.id,
            'ruleset_id': self.classic.id,
            'platform_id': self.console.id,
            'time': '1:20.63',
            'video': 'https://www.youtube.com/watch?v=123456'
        })

        response = self.create_submission_endpoint.handle_request(request)
        data = response.get_data()

        submission = data['submission']

        self.assertEqual(1, submission['id'])
        self.assertEqual(self.garma.id, submission['player_id'])
        self.assertEqual(self.crash_cove.id, submission['track_id'])
        self.assertEqual(self.course.id, submission['category_id'])
        self.assertEqual(self.dingodile.id, submission['character_id'])
        self.assertEqual(self.pal.id, submission['game_version_id'])
        self.assertEqual(self.classic.id, submission['ruleset_id'])
        self.assertEqual(self.console.id, submission['platform_id'])
        self.assertEqual(80.63, submission['time'])
        self.assertEqual('https://www.youtube.com/watch?v=123456', submission['video'])
        self.assertIsNotNone(submission['date'])

    def test_can_not_create_submission_if_no_track(self):
        request = Request.from_values(json={
            'category_id': self.course.id,
            'character_id': self.dingodile.id,
            'game_version_id': self.pal.id,
            'ruleset_id': self.classic.id,
            'platform_id': self.console.id,
            'time': '1:20.63',
            'video': 'https://www.youtube.com/watch?v=123456'
        })

        response = self.create_submission_endpoint.handle_request(request)
        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_create_submission_if_no_category(self):
        request = Request.from_values(json={
            'track_id': self.crash_cove.id,
            'character_id': self.dingodile.id,
            'game_version_id': self.pal.id,
            'ruleset_id': self.classic.id,
            'platform_id': self.console.id,
            'time': '1:20.63',
            'video': 'https://www.youtube.com/watch?v=123456'
        })

        response = self.create_submission_endpoint.handle_request(request)
        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_create_submission_if_no_character(self):
        request = Request.from_values(json={
            'track_id': self.crash_cove.id,
            'category_id': self.course.id,
            'game_version_id': self.pal.id,
            'ruleset_id': self.classic.id,
            'platform_id': self.console.id,
            'time': '1:20.63',
            'video': 'https://www.youtube.com/watch?v=123456'
        })

        response = self.create_submission_endpoint.handle_request(request)
        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_create_submission_if_no_game_version(self):
        request = Request.from_values(json={
            'track_id': self.crash_cove.id,
            'category_id': self.course.id,
            'character_id': self.dingodile.id,
            'ruleset_id': self.classic.id,
            'platform_id': self.console.id,
            'time': '1:20.63',
            'video': 'https://www.youtube.com/watch?v=123456'
        })

        response = self.create_submission_endpoint.handle_request(request)
        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_create_submission_if_no_ruleset(self):
        request = Request.from_values(json={
            'track_id': self.crash_cove.id,
            'category_id': self.course.id,
            'character_id': self.dingodile.id,
            'game_version_id': self.pal.id,
            'platform_id': self.console.id,
            'time': '1:20.63',
            'video': 'https://www.youtube.com/watch?v=123456'
        })

        response = self.create_submission_endpoint.handle_request(request)
        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_create_submission_if_no_platform(self):
        request = Request.from_values(json={
            'track_id': self.crash_cove.id,
            'category_id': self.course.id,
            'character_id': self.dingodile.id,
            'game_version_id': self.pal.id,
            'ruleset_id': self.classic.id,
            'time': '1:20.63',
            'video': 'https://www.youtube.com/watch?v=123456'
        })

        response = self.create_submission_endpoint.handle_request(request)
        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_create_submission_if_no_time(self):
        request = Request.from_values(json={
            'track_id': self.crash_cove.id,
            'category_id': self.course.id,
            'character_id': self.dingodile.id,
            'game_version_id': self.pal.id,
            'ruleset_id': self.classic.id,
            'platform_id': self.console.id,
            'video': 'https://www.youtube.com/watch?v=123456'
        })

        response = self.create_submission_endpoint.handle_request(request)
        data = response.get_data()

        self.assertIsNotNone(data['error'])

    def test_can_not_create_submission_if_no_video(self):
        request = Request.from_values(json={
            'track_id': self.crash_cove.id,
            'category_id': self.course.id,
            'character_id': self.dingodile.id,
            'game_version_id': self.pal.id,
            'ruleset_id': self.classic.id,
            'platform_id': self.console.id,
            'time': '1:20.63'
        })

        response = self.create_submission_endpoint.handle_request(request)
        data = response.get_data()

        self.assertIsNotNone(data['error'])
