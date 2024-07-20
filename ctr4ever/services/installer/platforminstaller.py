# coding=utf-8

from typing import List

from ctr4ever.models.platform import Platform
from ctr4ever.models.repository.platformrepository import PlatformRepository
from ctr4ever.services.installer.installer import Installer


class PlatformInstaller(Installer):

    def __init__(self, platform_repository: PlatformRepository):
        self.platform_repository = platform_repository

    def _validate_entry(self, entry: dict):
        if not 'name' in entry or not entry['name']:
            raise ValueError('Platform name is required')

    def _parse_json(self, json_content: list[dict]) -> List[Platform]:
        platforms = []

        for entry in json_content:
            platforms.append(Platform(name=entry['name']))

        return platforms

    def _create_entries(self, platforms: List[Platform]) -> None:
        for platform in platforms:
            result = self.platform_repository.find_by(platform.name)

            if len(result) > 0:
                existing_platform = result[0]
                self.platform_repository.update(id=existing_platform.id, name=platform.name)
            else:
                self.platform_repository.create(platform.name)
