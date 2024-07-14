# coding=utf-8

from ctr4ever.models.repository.categoryrepository import CategoryRepository
from ctr4ever.models.repository.characterrepository import CharacterRepository
from ctr4ever.models.repository.gameversionrepository import GameVersionRepository
from ctr4ever.models.submission import Submission


class SubmissionManager(object):

    def __init__(
            self,
            category_repository: CategoryRepository,
            character_repository: CharacterRepository,
            game_version_repository: GameVersionRepository
    ):
        self.category_repository = category_repository
        self.character_repository = character_repository
        self.game_version_repository = game_version_repository

    def is_valid_submission(self, submission: Submission):
        submission_category = self.category_repository.find_one(submission.category_id)
        submission_character = self.character_repository.find_one(submission.character_id)
        submission_game_version = self.game_version_repository.find_one(submission.game_version_id)

        # Secret characters are not available in relic race
        if submission_category.name == 'Relic Race':
            relic_race_excluded_characters = [
                'Ripper Roo',
                'Papu Papu',
                'Komodo Joe',
                'Pinstripe',
                'Fake Crash',
                'N. Tropy',
                'Fast Penta Penguin',
                'Slow Penta Penguin'
            ]

            if submission_character.name in relic_race_excluded_characters:
                return False

        # Fast Penta is only available on PAL and NTSC-J
        if submission_character.name == 'Fast Penta Penguin':
            fast_penta_excluded_game_versions = ['NTSC-U']

            if submission_game_version.name in fast_penta_excluded_game_versions:
                return False

        # Slow Penta is only available on NTSC-U
        if submission_character.name == 'Slow Penta Penguin':
            slow_penta_excluded_game_versions = ['PAL', 'NTSC-J']

            if submission_game_version.name in slow_penta_excluded_game_versions:
                return False

        # The maximum time is 9:59.99
        if submission.time > 599.99:
            return False

        return True
