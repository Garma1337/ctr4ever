# coding=utf-8

from typing import List, Optional

from ctr4ever.models.repository.modelrepository import ModelRepository
from ctr4ever.models.standardtime import StandardTime


class StandardTimeRepository(ModelRepository):

    def find_by(
            self,
            standard_id: Optional[int] = None,
            track_id: Optional[int] = None,
            category_id: Optional[int] = None
    ) -> List[StandardTime]:
        return super().find_by(
            standard_id=standard_id,
            track_id=track_id,
            category_id=category_id
        )

    def create(
            self,
            standard_id: int,
            track_id: int,
            category_id: int,
            time: float,
            numeric_value: int
    ) -> StandardTime:
        return super().create(
            standard_id=standard_id,
            track_id=track_id,
            category_id=category_id,
            time=time,
            numeric_value=numeric_value
        )

    def update(
            self,
            id: int,
            standard_id: Optional[int] = None,
            track_id: Optional[int] = None,
            category_id: Optional[int] = None,
            time: Optional[float] = None,
            numeric_value: Optional[int] = None
    ) -> None:
        super().update(
            id=id,
            standard_id=standard_id,
            track_id=track_id,
            category_id=category_id,
            time=time,
            numeric_value=numeric_value
        )

    def _get_model_class(self) -> type:
        return StandardTime
