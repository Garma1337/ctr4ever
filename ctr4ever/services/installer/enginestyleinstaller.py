# coding=utf-8

import json
from typing import List

from ctr4ever.helpers.filesystem import FileSystem
from ctr4ever.models.enginestyle import EngineStyle
from ctr4ever.models.repository.enginestylerepository import EngineStyleRepository
from ctr4ever.services.installer.installer import Installer


class EngineStyleInstaller(Installer):

    def __init__(self, engine_style_repository: EngineStyleRepository):
        self.engine_style_repository = engine_style_repository

    def install(self, file_name: str):
        if not FileSystem.file_exists(file_name):
            raise ValueError(f'File "{file_name}" does not exist')

        json_content = json.loads(FileSystem.read_file(file_name))

        for entry in json_content:
            self._validate_entry(entry)

        engine_styles = self._parse_engine_styles(json_content)
        self._upsert_engine_styles(engine_styles)

    def _upsert_engine_styles(self, engine_styles: List[EngineStyle]):
        for engine_style in engine_styles:
            result = self.engine_style_repository.find_by(engine_style.name)

            if len(result) > 0:
                existing_engine_style = result[0]
                self.engine_style_repository.update(id=existing_engine_style.id, name=engine_style.name)
            else:
                self.engine_style_repository.create(engine_style.name)

    def _parse_engine_styles(self, json_content: list[dict]) -> List[EngineStyle]:
        engine_styles: List[EngineStyle] = []

        for entry in json_content:
            engine_styles.append(EngineStyle(name=entry['name']))

        return engine_styles

    def _validate_entry(self, entry: dict):
        if not 'name' in entry or not entry['name']:
            raise ValueError('Engine style name is required')
