# coding=utf-8

from unittest import TestCase
from unittest.mock import Mock

from ctr4ever.helpers.filesystem import FileSystem
from ctr4ever.models.track import Track
from ctr4ever.services.installer.trackinstaller import TrackInstaller
from ctr4ever.tests.mockmodelrepository import MockTrackRepository


class TrackInstallerTest(TestCase):

    def setUp(self):
        self.track_repository = MockTrackRepository()
        self.track_installer = TrackInstaller(self.track_repository)

    def test_can_install_tracks(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": "Crash Cove"}, {"name": "Blizzard Bluff"}]')

        self.track_installer.install('tracks.json')

        tracks = self.track_repository.find_by()

        self.assertEqual(2, len(tracks))
        self.assertEqual('Crash Cove', tracks[0].name)
        self.assertEqual('Blizzard Bluff', tracks[1].name)

    def test_can_not_install_tracks_if_file_does_not_exist(self):
        FileSystem.file_exists = Mock(return_value=False)

        with self.assertRaises(ValueError):
            self.track_installer.install('tracks.json')

    def test_can_not_install_tracks_if_validation_fails(self):
        FileSystem.file_exists = Mock(return_value=True)
        FileSystem.read_file = Mock(return_value='[{"name": ""}]')

        with self.assertRaises(ValueError):
            self.track_installer.install('tracks.json')

    def test_can_create_tracks(self):
        self.track_installer._create_entries([
            Track(name='Crash Cove'),
            Track(name='Blizzard Bluff')
        ])

        tracks = self.track_repository.find_by()

        self.assertEqual(2, len(tracks))
        self.assertEqual('Crash Cove', tracks[0].name)
        self.assertEqual('Blizzard Bluff', tracks[1].name)

    def test_can_update_existing_tracks(self):
        self.track_repository.create('Crash Cove')
        self.track_repository.create('Blizzard Bluff')

        self.track_installer._create_entries([
            Track(name='Crash Cove'),
            Track(name='Blizzard Bluff')
        ])

        tracks = self.track_repository.find_by()

        self.assertEqual(2, len(tracks))
        self.assertEqual('Crash Cove', tracks[0].name)
        self.assertEqual('Blizzard Bluff', tracks[1].name)

    def test_can_parse_tracks(self):
        tracks = self.track_installer._parse_json([
            {"name": "Crash Cove"}
        ])

        self.assertEqual(1, len(tracks))
        self.assertEqual('Crash Cove', tracks[0].name)

    def test_can_not_validate_track_if_name_is_missing(self):
        with self.assertRaises(ValueError):
            self.track_installer._validate_entry({})

    def test_can_not_validate_track_if_name_is_empty(self):
        with self.assertRaises(ValueError):
            self.track_installer._validate_entry({'name': ''})
