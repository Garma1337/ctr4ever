# coding=utf-8

import json
from typing import List

from ctr4ever.helpers.filesystem import FileSystem
from ctr4ever.models.gameversion import GameVersion
from ctr4ever.models.repository.gameversionrepository import GameVersionRepository
from ctr4ever.services.installer.installer import Installer


class GameVersionInstaller(Installer):

    def __init__(self, game_version_repository: GameVersionRepository):
        self.game_version_repository = game_version_repository

    def install(self, file_name: str):
        if not FileSystem.file_exists(file_name):
            raise ValueError(f'File "{file_name}" does not exist')

        json_content = json.loads(FileSystem.read_file(file_name))

        for entry in json_content:
            self._validate_entry(entry)

        game_versions = self._parse_game_versions(json_content)
        self._upsert_game_versions(game_versions)

    def _parse_game_versions(self, json_content: list[dict]) -> List[GameVersion]:
        game_versions: List[GameVersion] = []

        for entry in json_content:
            game_versions.append(
                GameVersion(name=entry['name'], icon=entry['icon'])
            )

        return game_versions

    def _upsert_game_versions(self, game_versions: List[GameVersion]):
        for game_version in game_versions:
            result = self.game_version_repository.find_by(game_version.name)

            if len(result) > 0:
                existing_game_version = result[0]
                self.game_version_repository.update(id=existing_game_version.id, name=game_version.name, icon=game_version.icon)
            else:
                self.game_version_repository.create(game_version.name, game_version.icon)

    def _validate_entry(self, entry: dict):
        if not 'name' in entry or not entry['name']:
            raise ValueError('Game version name is required')

        if not 'icon' in entry or not entry['icon']:
            raise ValueError('Game version icon is required')
