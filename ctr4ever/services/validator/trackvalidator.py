# coding=utf-8

from ctr4ever.models.repository.trackrepository import TrackRepository
from ctr4ever.services.validator.validator import Validator, ValidationError


class TrackValidator(Validator):

    def __init__(self, track_repository: TrackRepository):
        self.track_repository = track_repository

    def validate_track(self, name: str):
        self.validate_name(name)

    def validate_name(self, name: str):
        if not name:
            raise ValidationError('The track name cannot be empty.')

        existing_tracks = self.track_repository.find_by(name=name)

        if len(existing_tracks) > 0:
            raise ValidationError(f'A track with the name "{name}" already exists.')

    def validate_id(self, track_id: int):
        if not track_id:
            raise ValidationError('The track id cannot be empty.')

        track = self.track_repository.find_one(track_id)

        if not track:
            raise ValidationError(f'No track with the id "{track_id}" exists.')
