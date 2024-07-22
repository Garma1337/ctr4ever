# coding=utf-8

from datetime import datetime

from ctr4ever.models.repository.categoryrepository import CategoryRepository
from ctr4ever.models.repository.characterrepository import CharacterRepository
from ctr4ever.models.repository.gameversionrepository import GameVersionRepository
from ctr4ever.models.repository.platformrepository import PlatformRepository
from ctr4ever.models.repository.playerrepository import PlayerRepository
from ctr4ever.models.repository.rulesetrepository import RulesetRepository
from ctr4ever.models.repository.submissionrepository import SubmissionRepository
from ctr4ever.models.repository.trackrepository import TrackRepository
from ctr4ever.models.submission import Submission


class SubmissionError(Exception):
    pass


class SubmissionManager(object):

    def __init__(
            self,
            category_repository: CategoryRepository,
            character_repository: CharacterRepository,
            game_version_repository: GameVersionRepository,
            platform_repository: PlatformRepository,
            player_repository: PlayerRepository,
            ruleset_repository: RulesetRepository,
            submission_repository: SubmissionRepository,
            track_repository: TrackRepository
    ):
        self.category_repository = category_repository
        self.character_repository = character_repository
        self.game_version_repository = game_version_repository
        self.platform_repository = platform_repository
        self.player_repository = player_repository
        self.ruleset_repository = ruleset_repository
        self.submission_repository = submission_repository
        self.track_repository = track_repository

    def is_valid_submission(
            self,
            category_id: int,
            character_id: int,
            game_version_id: int,
            time: float
    ) -> bool:
        submission_category = self.category_repository.find_one(category_id)
        submission_character = self.character_repository.find_one(character_id)
        submission_game_version = self.game_version_repository.find_one(game_version_id)

        if not submission_category or not submission_character or not submission_game_version:
            return False

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
        if time > 599.99:
            return False

        return True

    def submit_time(
            self,
            player_id: int,
            track_id: int,
            category_id: int,
            character_id: int,
            game_version_id: int,
            ruleset_id: int,
            platform_id: int,
            time: float,
            video: str
    ) -> Submission:
        submission_player = self.player_repository.find_one(player_id)
        submission_track = self.track_repository.find_one(track_id)
        submission_category = self.category_repository.find_one(category_id)
        submission_character = self.character_repository.find_one(character_id)
        submission_game_version = self.game_version_repository.find_one(game_version_id)
        submission_ruleset = self.ruleset_repository.find_one(ruleset_id)
        submission_platform = self.platform_repository.find_one(platform_id)

        if not submission_player:
            raise SubmissionError(f'No player with id "{player_id}" exists.')

        if not submission_track:
            raise SubmissionError(f'No track with id "{track_id}" exists.')

        if not submission_category:
            raise SubmissionError(f'No category with id "{category_id}" exists.')

        if not submission_character:
            raise SubmissionError(f'No character with id "{character_id}" exists.')

        if not submission_game_version:
            raise SubmissionError(f'No game version with id "{game_version_id}" exists.')

        if not submission_ruleset:
            raise SubmissionError(f'No ruleset with id "{ruleset_id}" exists.')

        if not submission_platform:
            raise SubmissionError(f'No platform with id "{platform_id}" exists.')

        if not self.is_valid_submission(category_id, character_id, game_version_id, time):
            raise SubmissionError('The submission is not valid.')

        submission = self.submission_repository.create(
            player_id=player_id,
            track_id=track_id,
            category_id=category_id,
            character_id=character_id,
            game_version_id=game_version_id,
            ruleset_id=ruleset_id,
            platform_id=platform_id,
            time=time,
            date=datetime.now(),
            video=video
        )

        return submission
