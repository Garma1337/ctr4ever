# coding=utf-8

from datetime import datetime
from unittest import TestCase

from ctr4ever.services.passwordmanager import PasswordManager
from ctr4ever.services.timeformatter import TimeFormatter
from ctr4ever.services.validator.categoryvalidator import CategoryValidator
from ctr4ever.services.validator.charactervalidator import CharacterValidator
from ctr4ever.services.validator.gameversionvalidator import GameVersionValidator
from ctr4ever.services.validator.platformvalidator import PlatformValidator
from ctr4ever.services.validator.playervalidator import PlayerValidator
from ctr4ever.services.validator.rulesetvalidator import RulesetValidator
from ctr4ever.services.validator.submissionvalidator import SubmissionValidator
from ctr4ever.services.validator.trackvalidator import TrackValidator
from ctr4ever.services.validator.validator import ValidationError
from ctr4ever.tests.mockmodelrepository import MockSubmissionRepository, MockTrackRepository, MockRulesetRepository, \
    MockPlayerRepository, MockPlatformRepository, MockGameVersionRepository, MockCharacterRepository, \
    MockCategoryRepository, MockEngineStyleRepository, MockCountryRepository
from ctr4ever.tests.mockpasswordencoderstrategy import MockPasswordEncoderStrategy


class SubmissionValidatorTest(TestCase):

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

    def test_can_validate_submission(self):
        self.submission_validator.validate_submission(
            self.garma.id,
            self.crash_cove.id,
            self.course.id,
            self.dingodile.id,
            self.ntscj.id,
            self.classic.id,
            self.console.id,
            '1:18.93',
            'https://www.youtube.com/watch?v=123456',
            'This is a comment'
        )

    def test_can_not_validate_submission_if_player_does_not_exist(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_submission(
                2,
                self.crash_cove.id,
                self.course.id,
                self.dingodile.id,
                self.ntscj.id,
                self.classic.id,
                self.console.id,
                '1:18.93',
                'https://www.youtube.com/watch?v=123456',
                'This is a comment'
            )

    def test_can_not_validate_submission_if_track_does_not_exist(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_submission(
                self.garma.id,
                2,
                self.course.id,
                self.dingodile.id,
                self.ntscj.id,
                self.classic.id,
                self.console.id,
                '1:18.93',
                'https://www.youtube.com/watch?v=123456',
                'This is a comment'
            )

    def test_can_not_validate_submission_if_category_does_not_exist(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_submission(
                self.garma.id,
                self.crash_cove.id,
                5,
                self.dingodile.id,
                self.ntscj.id,
                self.classic.id,
                self.console.id,
                '1:18.93',
                'https://www.youtube.com/watch?v=123456',
                'This is a comment'
            )

    def test_can_not_validate_submission_if_character_does_not_exist(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_submission(
                self.garma.id,
                self.crash_cove.id,
                self.course.id,
                5,
                self.ntscj.id,
                self.classic.id,
                self.console.id,
                '1:18.93',
                'https://www.youtube.com/watch?v=123456',
                'This is a comment'
            )

    def test_can_not_validate_submission_if_game_version_does_not_exist(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_submission(
                self.garma.id,
                self.crash_cove.id,
                self.course.id,
                self.dingodile.id,
                5,
                self.classic.id,
                self.console.id,
                '1:18.93',
                'https://www.youtube.com/watch?v=123456',
                'This is a comment'
            )

    def test_can_not_validate_submission_if_ruleset_does_not_exist(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_submission(
                self.garma.id,
                self.crash_cove.id,
                self.course.id,
                self.dingodile.id,
                self.ntscj.id,
                2,
                self.console.id,
                '1:18.93',
                'https://www.youtube.com/watch?v=123456',
                'This is a comment'
            )

    def test_can_not_validate_submission_if_platform_does_not_exist(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_submission(
                self.garma.id,
                self.crash_cove.id,
                self.course.id,
                self.dingodile.id,
                self.ntscj.id,
                self.classic.id,
                2,
                '1:18.93',
                'https://www.youtube.com/watch?v=123456',
                'This is a comment'
            )

    def test_can_not_validate_submission_if_secret_character_is_used_for_relic_race(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_submission(
                self.garma.id,
                self.crash_cove.id,
                self.relic_race.id,
                self.fake_crash.id,
                self.ntscj.id,
                self.classic.id,
                self.console.id,
                '29.51',
                'https://www.youtube.com/watch?v=123456',
                'This is a comment'
            )

    def test_can_not_validate_submission_if_slow_penta_is_used_in_ntsj_or_pal(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_submission(
                self.garma.id,
                self.crash_cove.id,
                self.course.id,
                self.slow_penta.id,
                self.ntscj.id,
                self.classic.id,
                self.console.id,
                '1:18.93',
                'https://www.youtube.com/watch?v=123456',
                'This is a comment'
            )

    def test_can_not_validate_submission_if_fast_penta_is_used_in_ntscu(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_submission(
                self.garma.id,
                self.crash_cove.id,
                self.course.id,
                self.fast_penta.id,
                self.ntscu.id,
                self.classic.id,
                self.console.id,
                '1:18.93',
                'https://www.youtube.com/watch?v=123456',
                'This is a comment'
            )

    def test_can_not_validate_submission_if_time_is_invalid(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_submission(
                self.garma.id,
                self.crash_cove.id,
                self.course.id,
                self.dingodile.id,
                self.ntscj.id,
                self.classic.id,
                self.console.id,
                '1:18:93',
                'https://www.youtube.com/watch?v=123456',
                'This is a comment'
            )

    def test_can_not_validate_submission_if_time_exceeds_maximum_time(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_submission(
                self.garma.id,
                self.crash_cove.id,
                self.course.id,
                self.dingodile.id,
                self.ntscj.id,
                self.classic.id,
                self.console.id,
                '10:00.00',
                'https://www.youtube.com/watch?v=123456',
                'This is a comment'
            )

    def test_can_not_validate_submission_if_video_is_empty(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_submission(
                self.garma.id,
                self.crash_cove.id,
                self.course.id,
                self.dingodile.id,
                self.ntscj.id,
                self.classic.id,
                self.console.id,
                '1:18.93',
                '',
                'This is a comment'
            )

    def test_can_not_validate_submission_if_video_is_invalid_youtube_video_link(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_submission(
                self.garma.id,
                self.crash_cove.id,
                self.course.id,
                self.dingodile.id,
                self.ntscj.id,
                self.classic.id,
                self.console.id,
                '1:18.93',
                'https://www.youtube.com/',
                'This is a comment'
            )

    def test_can_not_validate_submission_if_comment_length_exceeds_maximum_length(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_submission(
                self.garma.id,
                self.crash_cove.id,
                self.course.id,
                self.dingodile.id,
                self.ntscj.id,
                self.classic.id,
                self.console.id,
                '1:18.93',
                'https://www.youtube.com/watch?v=123456',
                ''.join(['a' for _ in range(1001)])
            )

    def test_can_not_validate_submission_if_submission_id_is_empty(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_id('')

    def test_can_not_validate_nonexistent_submission_id(self):
        with self.assertRaises(ValidationError) as context:
            self.submission_validator.validate_id(1)
