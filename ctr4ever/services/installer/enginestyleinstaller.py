# coding=utf-8

from typing import List

from ctr4ever.models.enginestyle import EngineStyle
from ctr4ever.models.repository.enginestylerepository import EngineStyleRepository
from ctr4ever.services.installer.installer import Installer


class EngineStyleInstaller(Installer):

    def __init__(self, engine_style_repository: EngineStyleRepository):
        self.engine_style_repository = engine_style_repository

    def _validate_entry(self, entry: dict):
        if not 'name' in entry or not entry['name']:
            raise ValueError('Engine style name is required')

    def _parse_json(self, json_content: list[dict]) -> List[EngineStyle]:
        engine_styles: List[EngineStyle] = []

        for entry in json_content:
            engine_styles.append(EngineStyle(name=entry['name']))

        return engine_styles

    def _create_entries(self, engine_styles: List[EngineStyle]) -> None:
        for engine_style in engine_styles:
            result = self.engine_style_repository.find_by(engine_style.name)

            if len(result) > 0:
                existing_engine_style = result[0]
                self.engine_style_repository.update(id=existing_engine_style.id, name=engine_style.name)
            else:
                self.engine_style_repository.create(engine_style.name)
