# coding=utf-8

from datetime import datetime
from typing import Optional

from ctr4ever.models.character import Character
from ctr4ever.models.repository.characterrepository import CharacterRepository
from ctr4ever.models.repository.submissionhistoryrepository import SubmissionHistoryRepository
from ctr4ever.models.repository.submissionrepository import SubmissionRepository
from ctr4ever.models.submission import Submission
from ctr4ever.services.timeformatter import TimeFormatter
from ctr4ever.services.validator.submissionvalidator import SubmissionValidator


class SubmissionError(Exception):
    pass


class SubmissionManager(object):

    def __init__(
            self,
            character_repository: CharacterRepository,
            submission_repository: SubmissionRepository,
            submission_history_repository: SubmissionHistoryRepository,
            submission_validator: SubmissionValidator,
            time_formatter: TimeFormatter
    ):
        self.character_repository = character_repository
        self.submission_repository = submission_repository
        self.submission_history_repository = submission_history_repository
        self.submission_validator = submission_validator
        self.time_formatter = time_formatter

    def submit_time(
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
    ) -> Submission:
        self.submission_validator.validate_submission(
            player_id,
            track_id,
            category_id,
            character_id,
            game_version_id,
            ruleset_id,
            platform_id,
            time,
            video,
            comment
        )

        parsed_time = self.time_formatter.create_time_from_format(time)

        existing_submissions = self.submission_repository.find_by(
            player_id=player_id,
            track_id=track_id,
            category_id=category_id,
            character_id=character_id,
            game_version_id=game_version_id,
            ruleset_id=ruleset_id,
            platform_id=platform_id
        )

        if len(existing_submissions) > 0:
            character: Character = self.character_repository.find_one(character_id)
            existing_submission = existing_submissions[0]
            existing_submission_character: Character = self.character_repository.find_one(existing_submission.character_id)

            if existing_submission_character.engine_style_id == character.engine_style_id:
                return self._update_submission(existing_submission.id, parsed_time.in_seconds(), video, comment)

        submission = self._create_submission(
            player_id,
            track_id,
            category_id,
            character_id,
            game_version_id,
            ruleset_id,
            platform_id,
            parsed_time.in_seconds(),
            video,
            comment
        )

        return submission

    def _create_submission(
            self,
            player_id: int,
            track_id: int,
            category_id: int,
            character_id: int,
            game_version_id: int,
            ruleset_id: int,
            platform_id: int,
            time: float,
            video: str,
            comment: Optional[str] = None
    ):
        return self.submission_repository.create(
            player_id,
            track_id,
            category_id,
            character_id,
            game_version_id,
            ruleset_id,
            platform_id,
            time,
            datetime.now(),
            video,
            comment
        )

    def _update_submission(self, submission_id: int, time: float, video: str, comment: Optional[str] = None) -> Submission:
        submission = self.submission_repository.find_one(submission_id)

        if not submission:
            raise SubmissionError(f'No submission with id "{submission_id}" exists.')

        self.submission_history_repository.create(
            player_id=submission.player_id,
            track_id=submission.track_id,
            category_id=submission.category_id,
            character_id=submission.character_id,
            game_version_id=submission.game_version_id,
            ruleset_id=submission.ruleset_id,
            platform_id=submission.platform_id,
            time=submission.time,
            date=submission.date,
            video=submission.video,
            comment=submission.comment
        )

        self.submission_repository.update(
            submission_id,
            time=time,
            video=video,
            comment=comment
        )

        return self.submission_repository.find_one(submission_id)
