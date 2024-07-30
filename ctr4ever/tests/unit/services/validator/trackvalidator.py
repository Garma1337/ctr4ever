# coding=utf-8

from unittest import TestCase

from ctr4ever.services.validator.trackvalidator import TrackValidator
from ctr4ever.services.validator.validator import ValidationError
from ctr4ever.tests.mockmodelrepository import MockTrackRepository


class TrackValidatorTest(TestCase):

    def setUp(self):
        self.track_repository = MockTrackRepository()
        self.track_validator = TrackValidator(self.track_repository)

    def test_can_validate_track_name(self):
        self.track_validator.validate_name('Crash Cove')

    def test_can_not_validate_empty_track_name(self):
        with self.assertRaises(ValidationError):
            self.track_validator.validate_name('')

    def test_can_not_validate_existing_track_name(self):
        self.track_repository.create('Crash Cove')

        with self.assertRaises(ValidationError):
            self.track_validator.validate_name('Crash Cove')

    def test_can_validate_track_id(self):
        track = self.track_repository.create('Crash Cove')

        self.track_validator.validate_id(track.id)

    def test_can_not_validate_empty_track_id(self):
        with self.assertRaises(ValidationError):
            self.track_validator.validate_id(None)

    def test_can_not_validate_nonexistent_track_id(self):
        with self.assertRaises(ValidationError):
            self.track_validator.validate_id(1)
