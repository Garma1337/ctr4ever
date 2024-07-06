# coding=utf-8

from typing import List

from ctr4ever.models.repository.modelrepository import ModelRepository
from ctr4ever.models.track import Track


class TrackRepository(ModelRepository):

    def find_by(self, name: str) -> List[Track]:
        return super().find_by(name = name)

    def create(self, name: str) -> Track:
        return super().create(name = name)

    def _get_model_class(self) -> type:
        return Track
