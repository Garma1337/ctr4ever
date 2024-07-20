# coding=utf-8

import json
from abc import abstractmethod
from typing import List

from ctr4ever.helpers.filesystem import FileSystem
from ctr4ever.models.model import Model


class Installer(object):

    def install(self, file_name: str):
        if not FileSystem.file_exists(file_name):
            raise ValueError(f'File "{file_name}" does not exist')

        json_content = json.loads(FileSystem.read_file(file_name))

        for entry in json_content:
            self._validate_entry(entry)

        entries = self._parse_json(json_content)
        self._create_entries(entries)

    @abstractmethod
    def _validate_entry(self, entry: dict):
        pass

    @abstractmethod
    def _parse_json(self, json_content: list[dict]) -> List[Model]:
        pass

    @abstractmethod
    def _create_entries(self, entries: List[Model]) -> None:
        pass
