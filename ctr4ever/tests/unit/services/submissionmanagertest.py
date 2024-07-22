# coding=utf-8

from datetime import datetime
from unittest import TestCase

from ctr4ever.services.submissionmanager import SubmissionManager
from ctr4ever.tests.mockmodelrepository import MockCategoryRepository, MockCharacterRepository, \
    MockGameVersionRepository, MockEngineStyleRepository, MockPlatformRepository, MockRulesetRepository, \
    MockPlayerRepository, MockTrackRepository, MockSubmissionRepository, MockCountryRepository


class SubmissionManagerTest(TestCase):

    def setUp(self):
        self.category_repository = MockCategoryRepository()
        self.character_repository = MockCharacterRepository()
        self.country_repository = MockCountryRepository()
        self.engine_style_repository = MockEngineStyleRepository()
        self.game_version_repository = MockGameVersionRepository()
        self.platform_repository = MockPlatformRepository()
        self.player_repository = MockPlayerRepository()
        self.ruleset_repository = MockRulesetRepository()
        self.submission_repository = MockSubmissionRepository()
        self.track_repository = MockTrackRepository()

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

        self.germany = self.country_repository.create('Germany', 'de.png')
        self.garma = self.player_repository.create(
            self.germany.id,
            'Garma',
            'test@test.com',
            '123456',
            '123456',
            True,
            datetime.now()
        )

        self.pal = self.game_version_repository.create('PAL', 'pal.png')
        self.ntscu = self.game_version_repository.create('NTSC-U', 'ntscu.png')
        self.ntscj = self.game_version_repository.create('NTSC-J', 'ntscj.png')

        self.course_category = self.category_repository.create('Course')
        self.relic_race_category = self.category_repository.create('Relic Race')

        self.max_engine = self.engine_style_repository.create('Max')
        self.speed_engine = self.engine_style_repository.create('Speed')
        self.turn_engine = self.engine_style_repository.create('Turning')

        self.dingodile = self.character_repository.create('Dingodile', self.speed_engine.id, 'dingo.png')
        self.fake_crash = self.character_repository.create('Fake Crash', self.max_engine.id, 'fake.png')
        self.fast_penta = self.character_repository.create('Fast Penta Penguin', self.max_engine.id, 'fast.png')
        self.slow_penta = self.character_repository.create('Slow Penta Penguin', self.max_engine.id, 'slow.png')

        self.classic = self.ruleset_repository.create('Classic')

        self.console = self.platform_repository.create('Console')
        self.crash_cove = self.track_repository.create('Crash Cove')

    def test_can_validate_submission(self):
        category_id = self.course_category.id
        character_id = self.dingodile.id
        game_version_id = self.pal.id
        time = 80.63

        self.assertTrue(self.submission_manager.is_valid_submission(category_id, character_id, game_version_id, time))

    def test_can_not_validate_submission_when_character_is_not_available_for_category(self):
        category_id = self.relic_race_category.id
        character_id = self.fake_crash.id
        game_version_id = self.pal.id
        time = 80.63

        self.assertFalse(self.submission_manager.is_valid_submission(category_id, character_id, game_version_id, time))

    def test_can_not_validate_submission_when_fast_penta_is_not_available_for_game_version(self):
        category_id = self.course_category.id
        character_id = self.fast_penta.id
        game_version_id = self.ntscu.id
        time = 80.63

        self.assertFalse(self.submission_manager.is_valid_submission(category_id, character_id, game_version_id, time))

    def test_can_not_validate_submission_when_slow_penta_is_not_available_for_game_version(self):
        category_id = self.course_category.id
        character_id = self.slow_penta.id
        game_version_id = self.pal.id
        time = 80.63

        self.assertFalse(self.submission_manager.is_valid_submission(category_id, character_id, game_version_id, time))

    def test_can_not_validate_submission_when_time_is_greater_than_maximum(self):
        category_id = self.course_category.id
        character_id = self.dingodile.id
        game_version_id = self.pal.id
        time = 600.00

        self.assertFalse(self.submission_manager.is_valid_submission(category_id, character_id, game_version_id, time))

    def test_can_not_validate_submission_when_dependencies_dont_exist(self):
        category_id = 999
        character_id = 999
        game_version_id = 999

        self.assertFalse(self.submission_manager.is_valid_submission(category_id, character_id, game_version_id, 100))

    def test_can_submit_time(self):
        player_id = self.garma.id
        track_id = self.crash_cove.id
        category_id = self.course_category.id
        character_id = self.dingodile.id
        game_version_id = self.pal.id
        ruleset_id = self.classic.id
        platform_id = self.console.id
        time = 80.63
        video = 'https://www.youtube.com/watch?v=123456'

        submission = self.submission_manager.submit_time(
            player_id,
            track_id,
            category_id,
            character_id,
            game_version_id,
            ruleset_id,
            platform_id,
            time,
            video
        )

        self.assertEqual(1, submission.id)
        self.assertEqual(player_id, submission.player_id)
        self.assertEqual(track_id, submission.track_id)
        self.assertEqual(category_id, submission.category_id)
        self.assertEqual(character_id, submission.character_id)
        self.assertEqual(game_version_id, submission.game_version_id)
        self.assertEqual(ruleset_id, submission.ruleset_id)
        self.assertEqual(platform_id, submission.platform_id)
        self.assertEqual(time, submission.time)
        self.assertEqual(video, submission.video)
        self.assertIsNotNone(submission.date)

    def test_can_not_submit_time_when_player_does_not_exist(self):
        player_id = 999
        track_id = self.crash_cove.id
        category_id = self.course_category.id
        character_id = self.dingodile.id
        game_version_id = self.pal.id
        ruleset_id = self.classic.id
        platform_id = self.console.id
        time = 80.63
        video = 'https://www.youtube.com/watch?v=123456'

        with self.assertRaises(Exception):
            self.submission_manager.submit_time(
                player_id,
                track_id,
                category_id,
                character_id,
                game_version_id,
                ruleset_id,
                platform_id,
                time,
                video
            )

    def test_can_not_submit_time_when_track_does_not_exist(self):
        player_id = self.garma.id
        track_id = 999
        category_id = self.course_category.id
        character_id = self.dingodile.id
        game_version_id = self.pal.id
        ruleset_id = self.classic.id
        platform_id = self.console.id
        time = 80.63
        video = 'https://www.youtube.com/watch?v=123456'

        with self.assertRaises(Exception):
            self.submission_manager.submit_time(
                player_id,
                track_id,
                category_id,
                character_id,
                game_version_id,
                ruleset_id,
                platform_id,
                time,
                video
            )

    def test_can_not_submit_time_when_category_does_not_exist(self):
        player_id = self.garma.id
        track_id = self.crash_cove.id
        category_id = 999
        character_id = self.dingodile.id
        game_version_id = self.pal.id
        ruleset_id = self.classic.id
        platform_id = self.console.id
        time = 80.63
        video = 'https://www.youtube.com/watch?v=123456'

        with self.assertRaises(Exception):
            self.submission_manager.submit_time(
                player_id,
                track_id,
                category_id,
                character_id,
                game_version_id,
                ruleset_id,
                platform_id,
                time,
                video
            )

    def test_can_not_submit_time_when_character_does_not_exist(self):
        player_id = self.garma.id
        track_id = self.crash_cove.id
        category_id = self.course_category.id
        character_id = 999
        game_version_id = self.pal.id
        ruleset_id = self.classic.id
        platform_id = self.console.id
        time = 80.63
        video = 'https://www.youtube.com/watch?v=123456'

        with self.assertRaises(Exception):
            self.submission_manager.submit_time(
                player_id,
                track_id,
                category_id,
                character_id,
                game_version_id,
                ruleset_id,
                platform_id,
                time,
                video
            )

    def test_can_not_submit_time_when_game_version_does_not_exist(self):
        player_id = self.garma.id
        track_id = self.crash_cove.id
        category_id = self.course_category.id
        character_id = self.dingodile.id
        game_version_id = 999
        ruleset_id = self.classic.id
        platform_id = self.console.id
        time = 80.63
        video = 'https://www.youtube.com/watch?v=123456'

        with self.assertRaises(Exception):
            self.submission_manager.submit_time(
                player_id,
                track_id,
                category_id,
                character_id,
                game_version_id,
                ruleset_id,
                platform_id,
                time,
                video
            )

    def test_can_not_submit_time_when_ruleset_does_not_exist(self):
        player_id = self.garma.id
        track_id = self.crash_cove.id
        category_id = self.course_category.id
        character_id = self.dingodile.id
        game_version_id = self.pal.id
        ruleset_id = 999
        platform_id = self.console.id
        time = 80.63
        video = 'https://www.youtube.com/watch?v=123456'

        with self.assertRaises(Exception):
            self.submission_manager.submit_time(
                player_id,
                track_id,
                category_id,
                character_id,
                game_version_id,
                ruleset_id,
                platform_id,
                time,
                video
            )

    def test_can_not_submit_time_when_platform_does_not_exist(self):
        player_id = self.garma.id
        track_id = self.crash_cove.id
        category_id = self.course_category.id
        character_id = self.dingodile.id
        game_version_id = self.pal.id
        ruleset_id = self.classic.id
        platform_id = 999
        time = 80.63
        video = 'https://www.youtube.com/watch?v=123456'

        with self.assertRaises(Exception):
            self.submission_manager.submit_time(
                player_id,
                track_id,
                category_id,
                character_id,
                game_version_id,
                ruleset_id,
                platform_id,
                time,
                video
            )
