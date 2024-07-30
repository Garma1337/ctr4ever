# coding=utf-8

from datetime import datetime
from unittest import TestCase

from ctr4ever.services.passwordmanager import PasswordManager
from ctr4ever.services.submissionmanager import SubmissionManager, SubmissionError
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
    MockGameVersionRepository, MockEngineStyleRepository, MockPlatformRepository, MockRulesetRepository, \
    MockPlayerRepository, MockTrackRepository, MockSubmissionRepository, MockCountryRepository, \
    MockSubmissionHistoryRepository
from ctr4ever.tests.mockpasswordencoderstrategy import MockPasswordEncoderStrategy


class SubmissionManagerTest(TestCase):

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

    def test_can_submit_time(self):
        submission = self.submission_manager.submit_time(
            self.garma.id,
            self.crash_cove.id,
            self.course.id,
            self.dingodile.id,
            self.pal.id,
            self.classic.id,
            self.console.id,
            '1:18.93',
            'https://www.youtube.com/watch?v=123456',
            'This is a test submission'
        )

        self.assertEqual(1, submission.id)
        self.assertEqual(self.garma.id, submission.player_id)
        self.assertEqual(self.crash_cove.id, submission.track_id)
        self.assertEqual(self.course.id, submission.category_id)
        self.assertEqual(self.dingodile.id, submission.character_id)
        self.assertEqual(self.pal.id, submission.game_version_id)
        self.assertEqual(self.classic.id, submission.ruleset_id)
        self.assertEqual(self.console.id, submission.platform_id)
        self.assertEqual(78.93, submission.time)
        self.assertEqual('https://www.youtube.com/watch?v=123456', submission.video)
        self.assertEqual('This is a test submission', submission.comment)

    def test_can_update_existing_submission(self):
        submission = self.submission_manager.submit_time(
            self.garma.id,
            self.crash_cove.id,
            self.course.id,
            self.dingodile.id,
            self.pal.id,
            self.classic.id,
            self.console.id,
            '1:18.93',
            'https://www.youtube.com/watch?v=123456',
            'This is a test submission'
        )

        submission = self.submission_manager.submit_time(
            self.garma.id,
            self.crash_cove.id,
            self.course.id,
            self.dingodile.id,
            self.pal.id,
            self.classic.id,
            self.console.id,
            '1:18.49',
            'https://www.youtube.com/watch?v=7891011',
            'This is an updated test submission'
        )

        self.assertEqual(1, submission.id)
        self.assertEqual(78.49, submission.time)
        self.assertEqual('https://www.youtube.com/watch?v=7891011', submission.video)
        self.assertEqual('This is an updated test submission', submission.comment)

    def test_can_not_update_existing_submission_when_different_engine(self):
        submission = self.submission_manager.submit_time(
            self.garma.id,
            self.crash_cove.id,
            self.course.id,
            self.dingodile.id,
            self.pal.id,
            self.classic.id,
            self.console.id,
            '1:18.93',
            'https://www.youtube.com/watch?v=123456',
            'This is a test submission'
        )

        submission = self.submission_manager.submit_time(
            self.garma.id,
            self.crash_cove.id,
            self.course.id,
            self.fake_crash.id,
            self.pal.id,
            self.classic.id,
            self.console.id,
            '1:18.49',
            'https://www.youtube.com/watch?v=7891011',
            'This is an updated test submission'
        )

        self.assertEqual(2, submission.id)
        self.assertEqual(self.garma.id, submission.player_id)
        self.assertEqual(self.crash_cove.id, submission.track_id)
        self.assertEqual(self.course.id, submission.category_id)
        self.assertEqual(self.fake_crash.id, submission.character_id)
        self.assertEqual(self.pal.id, submission.game_version_id)
        self.assertEqual(self.classic.id, submission.ruleset_id)
        self.assertEqual(self.console.id, submission.platform_id)
        self.assertEqual(78.49, submission.time)
        self.assertEqual('https://www.youtube.com/watch?v=7891011', submission.video)
        self.assertEqual('This is an updated test submission', submission.comment)

    def test_can_create_submission(self):
        submission = self.submission_manager._create_submission(
            self.garma.id,
            self.crash_cove.id,
            self.course.id,
            self.dingodile.id,
            self.pal.id,
            self.classic.id,
            self.console.id,
            78.93,
            'https://www.youtube.com/watch?v=123456',
            'This is a test submission'
        )

        self.assertEqual(1, submission.id)
        self.assertEqual(self.garma.id, submission.player_id)
        self.assertEqual(self.crash_cove.id, submission.track_id)
        self.assertEqual(self.course.id, submission.category_id)
        self.assertEqual(self.dingodile.id, submission.character_id)
        self.assertEqual(self.pal.id, submission.game_version_id)
        self.assertEqual(self.classic.id, submission.ruleset_id)
        self.assertEqual(self.console.id, submission.platform_id)
        self.assertEqual(78.93, submission.time)
        self.assertEqual('https://www.youtube.com/watch?v=123456', submission.video)
        self.assertEqual('This is a test submission', submission.comment)

    def test_can_update_submission(self):
        submission = self.submission_manager._create_submission(
            self.garma.id,
            self.crash_cove.id,
            self.course.id,
            self.dingodile.id,
            self.pal.id,
            self.classic.id,
            self.console.id,
            78.93,
            'https://www.youtube.com/watch?v=123456',
            'This is a test submission'
        )

        submission = self.submission_manager._update_submission(
            submission.id,
            78.49,
            'https://www.youtube.com/watch?v=7891011',
            'This is an updated test submission'
        )

        self.assertEqual(1, submission.id)
        self.assertEqual(78.49, submission.time)
        self.assertEqual('https://www.youtube.com/watch?v=7891011', submission.video)
        self.assertEqual('This is an updated test submission', submission.comment)

    def test_can_not_update_submission_when_submission_does_not_exist(self):
        with self.assertRaises(SubmissionError) as context:
            self.submission_manager._update_submission(
                1,
                78.49,
                'https://www.youtube.com/watch?v=7891011',
                'This is an updated test submission'
            )
