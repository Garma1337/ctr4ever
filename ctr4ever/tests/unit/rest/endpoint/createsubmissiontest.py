# coding=utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from flask import Request

from ctr4ever.rest.endpoint.createsubmission import CreateSubmission
from ctr4ever.services.passwordmanager import PasswordManager
from ctr4ever.services.submissionmanager import SubmissionManager
from ctr4ever.services.timeformatter import TimeFormatter
from ctr4ever.services.validator.categoryvalidator import CategoryValidator
from ctr4ever.services.validator.charactervalidator import CharacterValidator
from ctr4ever.services.validator.gameversionvalidator import GameVersionValidator
from ctr4ever.services.validator.platformvalidator import PlatformValidator
from ctr4ever.services.validator.playervalidator import PlayerValidator
from ctr4ever.services.validator.rulesetvalidator import RulesetValidator
from ctr4ever.services.validator.submissionvalidator import SubmissionValidator
from ctr4ever.services.validator.trackvalidator import TrackValidator
from ctr4ever.tests.mockmodelrepository import MockCategoryRepository, MockCharacterRepository, \
    MockEngineStyleRepository, MockGameVersionRepository, MockPlatformRepository, MockPlayerRepository, \
    MockRulesetRepository, MockSubmissionRepository, MockTrackRepository, MockCountryRepository, \
    MockSubmissionHistoryRepository
from ctr4ever.tests.mockpasswordencoderstrategy import MockPasswordEncoderStrategy


class CreateSubmissionTest(TestCase):

    def setUp(self):
        self.password_manager = PasswordManager(MockPasswordEncoderStrategy())

        self.category_repository = MockCategoryRepository()
        self.character_repository = MockCharacterRepository()
        self.country_repository = MockCountryRepository()
        self.engine_style_repository = MockEngineStyleRepository()
        self.game_version_repository = MockGameVersionRepository()
        self.platform_repository = MockPlatformRepository()
        self.player_repository = MockPlayerRepository()
        self.ruleset_repository = MockRulesetRepository()
        self.track_repository = MockTrackRepository()
        self.submission_repository = MockSubmissionRepository()
        self.submission_history_repository = MockSubmissionHistoryRepository()

        self.category_validator = CategoryValidator(self.category_repository)
        self.character_validator = CharacterValidator(self.character_repository, self.engine_style_repository)
        self.game_version_validator = GameVersionValidator(self.game_version_repository)
        self.platform_validator = PlatformValidator(self.platform_repository)
        self.player_validator = PlayerValidator(self.country_repository, self.player_repository, self.password_manager)
        self.ruleset_validator = RulesetValidator(self.ruleset_repository)
        self.track_validator = TrackValidator(self.track_repository)

        self.time_formatter = TimeFormatter()

        self.submission_validator = SubmissionValidator(
            self.category_repository,
            self.character_repository,
            self.game_version_repository,
            self.submission_repository,
            self.category_validator,
            self.character_validator,
            self.game_version_validator,
            self.platform_validator,
            self.player_validator,
            self.ruleset_validator,
            self.track_validator,
            self.time_formatter,
            1000
        )

        self.submission_manager = SubmissionManager(
            self.character_repository,
            self.submission_repository,
            self.submission_history_repository,
            self.submission_validator,
            self.time_formatter
        )

        self.pal = self.game_version_repository.create('PAL', 'pal.png')
        self.ntscu = self.game_version_repository.create('NTSC-U', 'ntscu.png')
        self.ntscj = self.game_version_repository.create('NTSC-J', 'ntscj.png')

        self.course = self.category_repository.create('Course')
        self.relic_race = self.category_repository.create('Relic Race')

        self.max = self.engine_style_repository.create('Max')
        self.speed = self.engine_style_repository.create('Speed')
        self.turn = self.engine_style_repository.create('Turning')

        self.dingodile = self.character_repository.create('Dingodile', self.speed.id, 'dingo.png')
        self.fake_crash = self.character_repository.create('Fake Crash', self.max.id, 'fake.png')
        self.fast_penta = self.character_repository.create('Fast Penta Penguin', self.max.id, 'fast.png')
        self.slow_penta = self.character_repository.create('Slow Penta Penguin', self.max.id, 'slow.png')

        self.classic = self.ruleset_repository.create('Classic')

        self.console = self.platform_repository.create('Console')
        self.crash_cove = self.track_repository.create('Crash Cove')

        self.germany = self.country_repository.create('Germany', 'de.png')
        self.garma = self.player_repository.create(
            self.germany.id,
            'Garma',
            'test@test.com',
            'Password123!',
            '123456',
            True,
            datetime.now()
        )

        self.create_submission_endpoint = CreateSubmission(self.submission_manager, self.time_formatter, 1000)
        self.create_submission_endpoint._get_current_user = Mock(return_value=self.garma.to_dictionary())

    def test_can_create_submission(self):
        request = Request.from_values(json = {
            'track_id': self.crash_cove.id,
            'category_id': self.course.id,
            'character_id': self.dingodile.id,
            'game_version_id': self.pal.id,
            'ruleset_id': self.classic.id,
            'platform_id': self.console.id,
            'time': '1:18.93',
            'video': 'https://www.youtube.com/watch?v=123456',
            'comment': 'This is a comment'
        })

        response = self.create_submission_endpoint.handle_request(request)
        data = response.get_data()

        submission = data['submission']

        self.assertEqual(submission['player_id'], self.garma.id)
        self.assertEqual(submission['track_id'], self.crash_cove.id)
        self.assertEqual(submission['category_id'], self.course.id)
        self.assertEqual(submission['character_id'], self.dingodile.id)
        self.assertEqual(submission['game_version_id'], self.pal.id)
        self.assertEqual(submission['ruleset_id'], self.classic.id)
        self.assertEqual(submission['platform_id'], self.console.id)
        self.assertEqual(submission['time'], 78.93)
        self.assertEqual(submission['video'], 'https://www.youtube.com/watch?v=123456')
        self.assertEqual(submission['comment'], 'This is a comment')

    def test_can_not_create_invalid_submission(self):
        request = Request.from_values(json = {
            'track_id': self.crash_cove.id,
            'category_id': self.relic_race.id,
            'character_id': self.fast_penta.id,
            'game_version_id': self.pal.id,
            'ruleset_id': self.classic.id,
            'platform_id': self.console.id,
            'time': '1:18.93',
            'video': 'https://www.youtube.com/watch?v=123456',
            'comment': 'This is a comment'
        })

        response = self.create_submission_endpoint.handle_request(request)
        data = response.get_data()

        self.assertIsNotNone(data['error'])
