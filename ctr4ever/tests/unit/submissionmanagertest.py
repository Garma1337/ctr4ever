# coding=utf-8

from unittest import TestCase

from ctr4ever.models.submission import Submission
from ctr4ever.services.submissionmanager import SubmissionManager
from ctr4ever.tests.mockmodelrepository import MockCategoryRepository, MockCharacterRepository, \
    MockGameVersionRepository, MockEngineStyleRepository


class SubmissionManagerTest(TestCase):

    def setUp(self):
        self.category_repository = MockCategoryRepository()
        self.character_repository = MockCharacterRepository()
        self.engine_style_repository = MockEngineStyleRepository()
        self.game_version_repository = MockGameVersionRepository()

        self.submission_manager = SubmissionManager(
            self.category_repository,
            self.character_repository,
            self.game_version_repository
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

    def test_can_validate_submission(self):
        submission = Submission(
            category_id = self.course_category.id,
            character_id = self.dingodile.id,
            game_version_id = self.pal.id,
            time = 80.63
        )

        self.assertTrue(self.submission_manager.is_valid_submission(submission))

    def test_can_not_validate_submission_when_character_is_not_available_for_category(self):
        submission = Submission(
            category_id = self.relic_race_category.id,
            character_id = self.fake_crash.id,
            game_version_id = self.pal.id,
            time = 80.63
        )

        self.assertFalse(self.submission_manager.is_valid_submission(submission))

    def test_can_not_validate_submission_when_fast_penta_is_not_available_for_game_version(self):
        submission = Submission(
            category_id = self.course_category.id,
            character_id = self.fast_penta.id,
            game_version_id = self.ntscu.id,
            time = 80.63
        )

        self.assertFalse(self.submission_manager.is_valid_submission(submission))

    def test_can_not_validate_submission_when_slow_penta_is_not_available_for_game_version(self):
        submission = Submission(
            category_id = self.course_category.id,
            character_id = self.slow_penta.id,
            game_version_id = self.pal.id,
            time = 80.63
        )

        self.assertFalse(self.submission_manager.is_valid_submission(submission))

    def test_can_not_validate_submission_when_time_is_greater_than_maximum(self):
        submission = Submission(
            category_id = self.course_category.id,
            character_id = self.dingodile.id,
            game_version_id = self.pal.id,
            time = 600.00
        )

        self.assertFalse(self.submission_manager.is_valid_submission(submission))
