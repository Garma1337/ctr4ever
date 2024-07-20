# coding=utf-8

from typing import List

from ctr4ever.models.gameversion import GameVersion
from ctr4ever.models.repository.gameversionrepository import GameVersionRepository
from ctr4ever.services.installer.installer import Installer


class GameVersionInstaller(Installer):

    def __init__(self, game_version_repository: GameVersionRepository):
        self.game_version_repository = game_version_repository

    def _validate_entry(self, entry: dict):
        if not 'name' in entry or not entry['name']:
            raise ValueError('Game version name is required')

        if not 'icon' in entry or not entry['icon']:
            raise ValueError('Game version icon is required')

    def _parse_json(self, json_content: list[dict]) -> List[GameVersion]:
        game_versions: List[GameVersion] = []

        for entry in json_content:
            game_versions.append(
                GameVersion(name=entry['name'], icon=entry['icon'])
            )

        return game_versions

    def _create_entries(self, game_versions: List[GameVersion]):
        for game_version in game_versions:
            result = self.game_version_repository.find_by(game_version.name)

            if len(result) > 0:
                existing_game_version = result[0]
                self.game_version_repository.update(
                    id=existing_game_version.id,
                    name=game_version.name,
                    icon=game_version.icon
                )
            else:
                self.game_version_repository.create(game_version.name, game_version.icon)
