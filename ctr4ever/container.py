# coding=utf-8

from flask import Flask

from ctr4ever import db
from ctr4ever.models.repository.categoryrepository import CategoryRepository
from ctr4ever.models.repository.characterrepository import CharacterRepository
from ctr4ever.models.repository.countryrepository import CountryRepository
from ctr4ever.models.repository.enginestylerepository import EngineStyleRepository
from ctr4ever.models.repository.gameversionrepository import GameVersionRepository
from ctr4ever.models.repository.platformrepository import PlatformRepository
from ctr4ever.models.repository.playerrepository import PlayerRepository
from ctr4ever.models.repository.rulesetrepository import RulesetRepository
from ctr4ever.models.repository.standardrepository import StandardRepository
from ctr4ever.models.repository.standardsetrepository import StandardSetRepository
from ctr4ever.models.repository.standardtimerepository import StandardTimeRepository
from ctr4ever.models.repository.trackrepository import TrackRepository
from ctr4ever.rest.endpoint.getplayer import GetPlayer
from ctr4ever.rest.requestdispatcher import RequestDispatcher
from ctr4ever.services.cache.memorycache import MemoryCache
from ctr4ever.services.container import Container
from ctr4ever.services.faker import Faker
from ctr4ever.services.installer.categoryinstaller import CategoryInstaller
from ctr4ever.services.installer.characterinstaller import CharacterInstaller
from ctr4ever.services.ranking_generator.afrankinggenerator import AFRankingGenerator
from ctr4ever.services.ranking_generator.arrrankinggenerator import ARRRankingGenerator
from ctr4ever.services.ranking_generator.srprrankinggenerator import SRPRRankingGenerator
from ctr4ever.services.ranking_generator.totaltimerankinggenerator import TotalTimeRankingGenerator
from ctr4ever.services.ranking_generator.uarrrankinggenerator import UARRRankingGenerator
from ctr4ever.services.standardcalculator import StandardCalculator
from ctr4ever.services.timeformatter import TimeFormatter

container = Container()


def init_app(app: Flask) -> Container:
    # api
    container.register('api.request_dispatcher', lambda: RequestDispatcher(container.get('container'), app.config))
    container.register('api.get_player_endpoint', lambda: GetPlayer(container.get('container'), app.config))

    # services
    container.register('services.faker', lambda: Faker(db))
    container.register('services.cache', lambda: MemoryCache())
    container.register('services.standard_calculator', lambda: StandardCalculator(container.get('time_formatter'), container.get('standard_time_repository')))
    container.register('services.time_formatter', lambda: TimeFormatter())

    # installer
    container.register('services.installer.category', lambda: CategoryInstaller(container.get('repository.category_repository')))
    container.register('services.installer.character', lambda: CharacterInstaller(
        container.get('repository.character_repository'),
        container.get('repository.engine_style_repository')
    ))

    # ranking
    container.register('service.ranking.af_ranking_generator', lambda: AFRankingGenerator())
    container.register('service.ranking.arr_ranking_generator', lambda: ARRRankingGenerator())
    container.register('service.ranking.srpr_ranking_generator', lambda: SRPRRankingGenerator())
    container.register('service.ranking.total_time_ranking_generator', lambda: TotalTimeRankingGenerator())
    container.register('service.ranking.uarr_ranking_generator', lambda: UARRRankingGenerator())

    # repositories
    container.register('repository.category_repository', lambda: CategoryRepository(db))
    container.register('repository.character_repository', lambda: CharacterRepository(db))
    container.register('repository.country_repository', lambda: CountryRepository(db))
    container.register('repository.engine_style_repository', lambda: EngineStyleRepository(db))
    container.register('repository.game_version_repository', lambda: GameVersionRepository(db))
    container.register('repository.platform_repository', lambda: PlatformRepository(db))
    container.register('repository.player_repository', lambda: PlayerRepository(db))
    container.register('repository.ruleset_repository', lambda: RulesetRepository(db))
    container.register('repository.standard_repository', lambda: StandardRepository(db))
    container.register('repository.standard_set_repository', lambda: StandardSetRepository(db))
    container.register('repository.standard_time_repository', lambda: StandardTimeRepository(db))
    container.register('repository.track_repository', lambda: TrackRepository(db))

    # container itself
    container.register('container', container)

    return container
