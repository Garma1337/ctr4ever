# coding=utf-8

from typing import List

from flask import Request

from ctr4ever.models.repository.trackrepository import TrackRepository
from ctr4ever.models.track import Track
from ctr4ever.rest.endpoint.endpoint import Endpoint
from ctr4ever.rest.response import Response


class FindTracks(Endpoint):

    def handle_request(self, request: Request) -> Response:
        track_repository: TrackRepository = self.container.get('repository.track')
        tracks: List[Track] = track_repository.find_by(name=request.args.get('name'))

        return Response({'tracks' : [track.to_dictionary() for track in tracks]})

    def get_accepted_request_method(self) -> str:
        return 'GET'
