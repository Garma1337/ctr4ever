# coding=utf-8

from typing import List

from ctr4ever.models.character import Character
from ctr4ever.models.repository.categoryrepository import CategoryRepository
from ctr4ever.models.repository.characterrepository import CharacterRepository
from ctr4ever.models.repository.countryrepository import CountryRepository
from ctr4ever.models.repository.enginestylerepository import EngineStyleRepository
from ctr4ever.models.repository.gameversionrepository import GameVersionRepository
from ctr4ever.models.repository.trackrepository import TrackRepository


class MasterData(object):

    def __init__(self,
        category_repository: CategoryRepository,
        character_repository: CharacterRepository,
        country_repository: CountryRepository,
        engine_style_repository: EngineStyleRepository,
        game_version_repository: GameVersionRepository,
        track_repository: TrackRepository
    ):
        self.category_repository = category_repository
        self.character_repository = character_repository
        self.country_repository = country_repository
        self.engine_style_repository = engine_style_repository
        self.game_version_repository = game_version_repository
        self.track_repository = track_repository

    def upsert_characters(self, characters: List[Character]) -> None:
        for character_data in characters:
            rows = self.engine_style_repository.find_by(name=character_data['engine'])

            if len(rows) <= 0:
                raise Exception(f'No engine {character_data['engine']} exists')

            engine = rows[0]

            self.character_repository.create(
                character_data['name'],
                engine.id,
                character_data['icon']
            )
