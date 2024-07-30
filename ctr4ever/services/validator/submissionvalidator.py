# coding=utf-8

from typing import Optional

from ctr4ever.models.category import Category
from ctr4ever.models.character import Character
from ctr4ever.models.gameversion import GameVersion
from ctr4ever.models.repository.categoryrepository import CategoryRepository
from ctr4ever.models.repository.characterrepository import CharacterRepository
from ctr4ever.models.repository.gameversionrepository import GameVersionRepository
from ctr4ever.models.repository.submissionrepository import SubmissionRepository
from ctr4ever.services.timeformatter import TimeFormatter
from ctr4ever.services.validator.categoryvalidator import CategoryValidator
from ctr4ever.services.validator.charactervalidator import CharacterValidator
from ctr4ever.services.validator.gameversionvalidator import GameVersionValidator
from ctr4ever.services.validator.platformvalidator import PlatformValidator
from ctr4ever.services.validator.playervalidator import PlayerValidator
from ctr4ever.services.validator.rulesetvalidator import RulesetValidator
from ctr4ever.services.validator.trackvalidator import TrackValidator
from ctr4ever.services.validator.validator import Validator, ValidationError


class SubmissionValidator(Validator):

    def __init__(
            self,
            category_repository: CategoryRepository,
            character_repository: CharacterRepository,
            game_version_repository: GameVersionRepository,
            submission_repository: SubmissionRepository,
            category_validator: CategoryValidator,
            character_validator: CharacterValidator,
            game_version_validator: GameVersionValidator,
            platform_validator: PlatformValidator,
            player_validator: PlayerValidator,
            ruleset_validator: RulesetValidator,
            track_validator: TrackValidator,
            time_formatter: TimeFormatter,
            max_comment_length: int
    ):
        self.category_repository = category_repository
        self.character_repository = character_repository
        self.game_version_repository = game_version_repository
        self.submission_repository = submission_repository
        self.category_validator = category_validator
        self.character_validator = character_validator
        self.game_version_validator = game_version_validator
        self.platform_validator = platform_validator
        self.player_validator = player_validator
        self.ruleset_validator = ruleset_validator
        self.track_validator = track_validator
        self.time_formatter = time_formatter
        self.max_comment_length = max_comment_length

    def validate_submission(
            self,
            player_id: int,
            track_id: int,
            category_id: int,
            character_id: int,
            game_version_id: int,
            ruleset_id: int,
            platform_id: int,
            time: str,
            video: str,
            comment: Optional[str] = None
    ):
        self.player_validator.validate_id(player_id)
        self.track_validator.validate_id(track_id)
        self.category_validator.validate_id(category_id)
        self.character_validator.validate_id(character_id)
        self.game_version_validator.validate_id(game_version_id)
        self.ruleset_validator.validate_id(ruleset_id)
        self.platform_validator.validate_id(platform_id)

        self.validate_category(category_id, character_id, game_version_id)

        self.validate_time(time)
        self.validate_video(video)
        self.validate_comment(comment)

    def validate_category(self, category_id: int, character_id: int, game_version_id: int):
        category: Category = self.category_repository.find_one(category_id)
        character: Character = self.character_repository.find_one(character_id)
        game_version: GameVersion = self.game_version_repository.find_one(game_version_id)

        if category.name == 'Relic Race':
            self.valid_relic_race_submission(character)

        if character.name == 'Fast Penta Penguin':
            self.validate_fast_penta_penguin_submission(character, game_version)

        if character.name == 'Slow Penta Penguin':
            self.validate_slow_penta_penguin_submission(character, game_version)

    def valid_relic_race_submission(self, character: Character):
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

        if character.name in relic_race_excluded_characters:
            raise ValidationError(f'The character {character.name} is not available for relic race.')

    def validate_fast_penta_penguin_submission(self, character: Character, game_version: GameVersion):
        fast_penta_excluded_game_versions = ['NTSC-U']

        if game_version.name in fast_penta_excluded_game_versions:
            raise ValidationError(
                f'The character {character.name} is not available in the {game_version.name} version of the game.')

    def validate_slow_penta_penguin_submission(self, character: Character, game_version: GameVersion):
        slow_penta_excluded_game_versions = ['PAL', 'NTSC-J']

        if game_version.name in slow_penta_excluded_game_versions:
            raise ValidationError(
                f'The character {character.name} is not available in the {game_version.name} version of the game.')

    def validate_time(self, time: str):
        parsed_time = self.time_formatter.create_time_from_format(time)

        if not parsed_time:
            raise ValidationError(f'{time} is not a valid time.')

        if parsed_time.in_seconds() > 599.99:
            raise ValidationError(f'The time {time} exceeds the maximum time of 9:59.99.')

    def validate_video(self, video: str):
        if not video:
            raise ValidationError('The video cannot be empty.')

        if not 'https://www.youtube.com/watch?' in video:
            raise ValidationError('The video must be a valid YouTube video link.')

    def validate_comment(self, comment: Optional[str]):
        if not comment:
            return

        if len(comment) > self.max_comment_length:
            raise ValidationError(f'The comment length cannot exceed {self.max_comment_length} characters.')

    def validate_id(self, submission_id: int):
        if not submission_id:
            raise ValidationError('The submission id cannot be empty.')

        submission = self.submission_repository.find_one(submission_id)

        if not submission:
            raise ValidationError(f'No submission with the id "{submission_id}" exists.')
