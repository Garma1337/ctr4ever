# coding=utf-8

from flask import Flask

from ctr4ever import db
from ctr4ever.models.repository.categoryrepository import CategoryRepository
from ctr4ever.models.repository.characterrepository import CharacterRepository
from ctr4ever.models.repository.playerrepository import PlayerRepository
from ctr4ever.models.repository.standardrepository import StandardRepository
from ctr4ever.models.repository.standardtimerepository import StandardTimeRepository
from ctr4ever.models.repository.trackrepository import TrackRepository
from ctr4ever.rest.endpoint.getplayer import GetPlayer
from ctr4ever.rest.requestdispatcher import RequestDispatcher
from ctr4ever.services.cache.memorycache import MemoryCache
from ctr4ever.services.container import Container
from ctr4ever.services.fakerservice import FakerService
from ctr4ever.services.standardcalculator import StandardCalculator
from ctr4ever.services.timeparser import TimeParser

container = Container()


def init_app(app: Flask) -> Container:
    # api
    container.register('api.request_dispatcher', lambda: RequestDispatcher(container.get('container'), app.config))
    container.register('api.get_player_endpoint', lambda: GetPlayer(container.get('container'), app.config))

    # services
    container.register('services.time_parser', lambda: TimeParser())
    container.register('services.faker_service', lambda: FakerService(db))
    container.register('services.memory_cache', lambda: MemoryCache())
    container.register('services.standard_calculator', lambda: StandardCalculator(container.get('time_parser'), container.get('standard_time_repository')))

    # repositories
    container.register('repository.category_repository', lambda: CategoryRepository(db))
    container.register('repository.character_repository', lambda: CharacterRepository(db))
    container.register('repository.player_repository', lambda: PlayerRepository(db))
    container.register('repository.standard_repository', lambda: StandardRepository(db))
    container.register('repository.standard_time_repository', lambda: StandardTimeRepository(db))
    container.register('repository.track_repository', lambda: TrackRepository(db))

    # container itself
    container.register('container', container)

    return container
