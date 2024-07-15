# coding=utf-8

from unittest import TestCase

from flask import Config, Request

from ctr4ever.rest.endpoint.findtracks import FindTracks
from ctr4ever.services.container import Container
from ctr4ever.tests.mockmodelrepository import MockTrackRepository


class FindTracksTest(TestCase):

    def setUp(self):
        self.track_repository = MockTrackRepository()
        self.track_repository.create('Crash Cove')
        self.track_repository.create('Sewer Speedway')
        self.track_repository.create('Blizzard Bluff')

        self.container = Container()
        self.container.register('repository.track', lambda: self.track_repository)

        self.find_tracks_endpoint = FindTracks(self.container, Config(''))

    def test_can_find_tracks(self):
        request = Request.from_values()

        response = self.find_tracks_endpoint.handle_request(request)
        data = response.get_data()

        tracks = data['tracks']

        self.assertEqual(3, len(tracks))
        self.assertEqual('Crash Cove', tracks[0]['name'])
        self.assertEqual('Sewer Speedway', tracks[1]['name'])
        self.assertEqual('Blizzard Bluff', tracks[2]['name'])

    def test_can_find_tracks_filtered_by_name(self):
        request = Request.from_values(query_string='name=Crash Cove')

        response = self.find_tracks_endpoint.handle_request(request)
        data = response.get_data()

        tracks = data['tracks']

        self.assertEqual(1, len(tracks))
        self.assertEqual('Crash Cove', tracks[0]['name'])

    def test_can_find_tracks_filtered_by_name_not_found(self):
        request = Request.from_values(query_string='name=Crash Bandicoot')

        response = self.find_tracks_endpoint.handle_request(request)
        data = response.get_data()
