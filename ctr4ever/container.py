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
from ctr4ever.models.repository.submissionrepository import SubmissionRepository
from ctr4ever.models.repository.trackrepository import TrackRepository
from ctr4ever.rest.endpoint.authenticateplayer import AuthenticatePlayer
from ctr4ever.rest.endpoint.createsubmission import CreateSubmission
from ctr4ever.rest.endpoint.findcategories import FindCategories
from ctr4ever.rest.endpoint.findcharacters import FindCharacters
from ctr4ever.rest.endpoint.findcountries import FindCountries
from ctr4ever.rest.endpoint.findenginestyles import FindEngineStyles
from ctr4ever.rest.endpoint.findgameversions import FindGameVersions
from ctr4ever.rest.endpoint.findplatforms import FindPlatforms
from ctr4ever.rest.endpoint.findplayers import FindPlayers
from ctr4ever.rest.endpoint.findrulesets import FindRulesets
from ctr4ever.rest.endpoint.findsubmissions import FindSubmissions
from ctr4ever.rest.endpoint.findtracks import FindTracks
from ctr4ever.rest.endpoint.getsession import GetSession
from ctr4ever.rest.endpoint.loginplayer import LoginPlayer
from ctr4ever.rest.endpoint.registerplayer import RegisterPlayer
from ctr4ever.rest.requestdispatcher import RequestDispatcher
from ctr4ever.rest.routeresolver import RouteResolverFactory
from ctr4ever.services.authenticator import Authenticator
from ctr4ever.services.cache.memorycache import MemoryCache
from ctr4ever.services.container import Container
from ctr4ever.services.faker import Faker
from ctr4ever.services.installer.categoryinstaller import CategoryInstaller
from ctr4ever.services.installer.characterinstaller import CharacterInstaller
from ctr4ever.services.installer.countryinstaller import CountryInstaller
from ctr4ever.services.installer.enginestyleinstaller import EngineStyleInstaller
from ctr4ever.services.installer.gameversioninstaller import GameVersionInstaller
from ctr4ever.services.installer.platforminstaller import PlatformInstaller
from ctr4ever.services.installer.rulesetinstaller import RulesetInstaller
from ctr4ever.services.installer.trackinstaller import TrackInstaller
from ctr4ever.services.password_encoder_strategy.bcryptpasswordencoderstrategy import BcryptPasswordEncoderStrategy
from ctr4ever.services.passwordmanager import PasswordManager
from ctr4ever.services.ranking_generator.afrankinggenerator import AFRankingGenerator
from ctr4ever.services.ranking_generator.arrrankinggenerator import ARRRankingGenerator
from ctr4ever.services.ranking_generator.srprrankinggenerator import SRPRRankingGenerator
from ctr4ever.services.ranking_generator.totaltimerankinggenerator import TotalTimeRankingGenerator
from ctr4ever.services.ranking_generator.uarrrankinggenerator import UARRRankingGenerator
from ctr4ever.services.standardcalculator import StandardCalculator
from ctr4ever.services.submissionmanager import SubmissionManager
from ctr4ever.services.timeformatter import TimeFormatter

container = Container()

def init_app(app: Flask) -> Container:
    # api
    container.register('api.route_resolver', lambda: RouteResolverFactory.create(container.get('container')))
    container.register('api.request_dispatcher', lambda: RequestDispatcher(container.get('api.route_resolver')))
    container.register('api.endpoint.authenticate_player', lambda: AuthenticatePlayer(container.get('services.authenticator')))
    container.register('api.endpoint.create_submission', lambda: CreateSubmission(
        container.get('services.submission_manager'),
        container.get('services.time_formatter'),
        app.config.get('SUBMISSION_COMMENT_MAX_LENGTH')
    ))
    container.register('api.endpoint.find_categories', lambda: FindCategories(container.get('repository.category')))
    container.register('api.endpoint.find_characters', lambda: FindCharacters(container.get('repository.character')))
    container.register('api.endpoint.find_countries', lambda: FindCountries(container.get('repository.country')))
    container.register('api.endpoint.find_engine_styles', lambda: FindEngineStyles(container.get('repository.engine_style')))
    container.register('api.endpoint.find_game_versions', lambda: FindGameVersions(container.get('repository.game_version')))
    container.register('api.endpoint.find_platforms', lambda: FindPlatforms(container.get('repository.platform')))
    container.register('api.endpoint.find_players', lambda: FindPlayers(container.get('repository.player')))
    container.register('api.endpoint.find_rulesets', lambda: FindRulesets(container.get('repository.ruleset')))
    container.register('api.endpoint.find_submissions', lambda: FindSubmissions(container.get('repository.submission')))
    container.register('api.endpoint.find_tracks', lambda: FindTracks(container.get('repository.track')))
    container.register('api.endpoint.get_session', lambda: GetSession())
    container.register('api.endpoint.login_player', lambda: LoginPlayer(container.get('repository.player'), container.get('services.authenticator')))
    container.register('api.endpoint.register_player', lambda: RegisterPlayer(container.get('services.authenticator')))

    # services
    container.register('services.authenticator', lambda: Authenticator(
        container.get('services.password_manager'),
        container.get('repository.country'),
        container.get('repository.player')
    ))
    container.register('services.cache', lambda: MemoryCache())
    container.register('services.faker', lambda: Faker(db))
    container.register('services.password_encoder_strategy', lambda: BcryptPasswordEncoderStrategy())
    container.register('services.password_manager', lambda: PasswordManager(container.get('services.password_encoder_strategy')))
    container.register('services.standard_calculator', lambda: StandardCalculator(
        container.get('services.time_formatter'),
        container.get('repository.standard_time')
    ))
    container.register('services.submission_manager', lambda: SubmissionManager(
        container.get('repository.category'),
        container.get('repository.character'),
        container.get('repository.game_version'),
        container.get('repository.platform'),
        container.get('repository.player'),
        container.get('repository.ruleset'),
        container.get('repository.submission'),
        container.get('repository.track')
    ))
    container.register('services.time_formatter', lambda: TimeFormatter())

    # installer
    container.register('services.installer.category', lambda: CategoryInstaller(container.get('repository.category')))
    container.register('services.installer.character', lambda: CharacterInstaller(
        container.get('repository.character'),
        container.get('repository.engine_style')
    ))
    container.register('services.installer.country', lambda: CountryInstaller(container.get('repository.country')))
    container.register('services.installer.engine_style', lambda: EngineStyleInstaller(container.get('repository.engine_style')))
    container.register('services.installer.game_version', lambda: GameVersionInstaller(container.get('repository.game_version')))
    container.register('services.installer.platform', lambda: PlatformInstaller(container.get('repository.platform')))
    container.register('services.installer.ruleset', lambda: RulesetInstaller(container.get('repository.ruleset')))
    container.register('services.installer.track', lambda: TrackInstaller(container.get('repository.track')))

    # ranking
    container.register('services.ranking.af_ranking_generator', lambda: AFRankingGenerator())
    container.register('services.ranking.arr_ranking_generator', lambda: ARRRankingGenerator())
    container.register('services.ranking.srpr_ranking_generator', lambda: SRPRRankingGenerator())
    container.register('services.ranking.total_time_ranking_generator', lambda: TotalTimeRankingGenerator())
    container.register('services.ranking.uarr_ranking_generator', lambda: UARRRankingGenerator())

    # repositories
    container.register('repository.category', lambda: CategoryRepository(db))
    container.register('repository.character', lambda: CharacterRepository(db))
    container.register('repository.country', lambda: CountryRepository(db))
    container.register('repository.engine_style', lambda: EngineStyleRepository(db))
    container.register('repository.game_version', lambda: GameVersionRepository(db))
    container.register('repository.platform', lambda: PlatformRepository(db))
    container.register('repository.player', lambda: PlayerRepository(db))
    container.register('repository.ruleset', lambda: RulesetRepository(db))
    container.register('repository.standard', lambda: StandardRepository(db))
    container.register('repository.standard_set', lambda: StandardSetRepository(db))
    container.register('repository.standard_time', lambda: StandardTimeRepository(db))
    container.register('repository.submission', lambda: SubmissionRepository(db))
    container.register('repository.track', lambda: TrackRepository(db))

    # container itself
    container.register('container', lambda: container)

    return container
