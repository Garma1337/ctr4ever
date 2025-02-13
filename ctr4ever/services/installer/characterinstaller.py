# coding=utf-8

from typing import List

from ctr4ever.models.character import Character
from ctr4ever.models.repository.characterrepository import CharacterRepository
from ctr4ever.models.repository.enginestylerepository import EngineStyleRepository
from ctr4ever.services.installer.installer import Installer


class CharacterInstaller(Installer):

    def __init__(self, character_repository: CharacterRepository, engine_style_repository: EngineStyleRepository):
        self.character_repository = character_repository
        self.engine_style_repository = engine_style_repository

        self._engine_styles = self.engine_style_repository.find_by()

    def _validate_entry(self, entry: dict):
        if not 'name' in entry or not entry['name']:
            raise ValueError('Character name is required')

        if not 'icon' in entry or not entry['icon']:
            raise ValueError('Character icon is required')

        if not 'engine' in entry or not entry['engine']:
            raise ValueError('Character engine is required')

        engine_styles = [engine_style for engine_style in self._engine_styles if engine_style.name == entry['engine']]

        if len(engine_styles) <= 0:
            raise ValueError(f'Engine style "{entry["engine"]}" does not exist')

    def _parse_json(self, json_content: list[dict]) -> List[Character]:
        characters: List[Character] = []

        for entry in json_content:
            engine_styles = [engine_style for engine_style in self._engine_styles if engine_style.name == entry['engine']]

            characters.append(Character(
                name=entry['name'],
                icon=entry['icon'],
                engine_style_id=engine_styles[0].id
            ))

        return characters

    def _create_entries(self, characters: List[Character]) -> None:
        for character in characters:
            result = self.character_repository.find_by(character.name)

            if len(result) > 0:
                existing_character = result[0]

                self.character_repository.update(
                    id=existing_character.id,
                    name=character.name,
                    icon=character.icon,
                    engine_style_id=character.engine_style_id
                )
            else:
                self.character_repository.create(character.name, character.engine_style_id, character.icon)
