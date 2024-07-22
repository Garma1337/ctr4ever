# coding=utf-8

from datetime import datetime
from typing import List, Optional

from ctr4ever.models.repository.modelrepository import ModelRepository
from ctr4ever.models.submission import Submission


class SubmissionRepository(ModelRepository):

    def find_by(
            self,
            player_id: Optional[int] = None,
            track_id: Optional[int] = None,
            category_id: Optional[int] = None,
            character_id: Optional[int] = None,
            game_version_id: Optional[int] = None,
            ruleset_id: Optional[int] = None,
            platform_id: Optional[int] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None
    ) -> List[Submission]:
        return super().find_by(
            player_id=player_id,
            track_id=track_id,
            category_id=category_id,
            character_id=character_id,
            game_version_id=game_version_id,
            ruleset_id=ruleset_id,
            platform_id=platform_id,
            limit=limit,
            offset=offset
        )

    def count(
            self,
            player_id: Optional[int] = None,
            track_id: Optional[int] = None,
            category_id: Optional[int] = None,
            character_id: Optional[int] = None,
            game_version_id: Optional[int] = None,
            ruleset_id: Optional[int] = None,
            platform_id: Optional[int] = None,
    ) -> int:
        return super().count(
            player_id=player_id,
            track_id=track_id,
            category_id=category_id,
            character_id=character_id,
            game_version_id=game_version_id,
            ruleset_id=ruleset_id,
            platform_id=platform_id
        )

    def create(
            self,
            player_id: int,
            track_id: int,
            category_id: int,
            character_id: int,
            game_version_id: int,
            ruleset_id: int,
            platform_id: int,
            time: float,
            date: datetime,
            video: str
    ) -> Submission:
        return super().create(
            player_id=player_id,
            track_id=track_id,
            category_id=category_id,
            character_id=character_id,
            game_version_id=game_version_id,
            ruleset_id=ruleset_id,
            platform_id=platform_id,
            time=time,
            date=date,
            video=video
        )

    def update(
            self,
            id: int,
            player_id: Optional[int] = None,
            track_id: Optional[int] = None,
            category_id: Optional[int] = None,
            character_id: Optional[int] = None,
            game_version_id: Optional[int] = None,
            ruleset_id: Optional[int] = None,
            platform_id: Optional[int] = None,
            time: Optional[float] = None,
            date: Optional[datetime] = None,
            video: Optional[str] = None
    ) -> None:
        super().update(
            id=id,
            player_id=player_id,
            track_id=track_id,
            category_id=category_id,
            character_id=character_id,
            game_version_id=game_version_id,
            ruleset_id=ruleset_id,
            platform_id=platform_id,
            time=time,
            date=date,
            video=video
        )

    def _get_model_class(self) -> type:
        return Submission
