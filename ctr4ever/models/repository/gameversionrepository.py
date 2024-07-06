# coding=utf-8

from ctr4ever.models.gameversion import GameVersion
from ctr4ever.models.repository.modelrepository import ModelRepository


class GameVersionRepository(ModelRepository):

    def find_by(self, name: str):
        return super().find_by(name = name)

    def create(self, name: str) -> GameVersion:
        return super().create(name = name)

    def _get_model_class(self) -> type:
        return GameVersion
