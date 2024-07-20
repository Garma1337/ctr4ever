# coding=utf-8

from typing import List

from ctr4ever.models.repository.trackrepository import TrackRepository
from ctr4ever.models.track import Track
from ctr4ever.services.installer.installer import Installer


class TrackInstaller(Installer):

    def __init__(self, track_repository: TrackRepository):
        self.track_repository = track_repository

    def _validate_entry(self, entry: dict):
        if not 'name' in entry or not entry['name']:
            raise ValueError('Track name is required')

    def _parse_json(self, json_content: list[dict]) -> List[Track]:
        tracks = []

        for entry in json_content:
            tracks.append(Track(name=entry['name']))

        return tracks

    def _create_entries(self, tracks: List[Track]) -> None:
        for track in tracks:
            result = self.track_repository.find_by(track.name)

            if len(result) > 0:
                existing_track = result[0]
                self.track_repository.update(id=existing_track.id, name=track.name)
            else:
                self.track_repository.create(track.name)
