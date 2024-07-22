# coding=utf-8

from abc import abstractmethod
from datetime import datetime

from ctr4ever.models.category import Category
from ctr4ever.models.character import Character
from ctr4ever.models.country import Country
from ctr4ever.models.enginestyle import EngineStyle
from ctr4ever.models.gameversion import GameVersion
from ctr4ever.models.platform import Platform
from ctr4ever.models.player import Player
from ctr4ever.models.repository.categoryrepository import CategoryRepository
from ctr4ever.models.repository.characterrepository import CharacterRepository
from ctr4ever.models.repository.countryrepository import CountryRepository
from ctr4ever.models.repository.enginestylerepository import EngineStyleRepository
from ctr4ever.models.repository.gameversionrepository import GameVersionRepository
from ctr4ever.models.repository.modelrepository import ModelRepository
from ctr4ever.models.repository.platformrepository import PlatformRepository
from ctr4ever.models.repository.playerrepository import PlayerRepository
from ctr4ever.models.repository.rulesetrepository import RulesetRepository
from ctr4ever.models.repository.standardrepository import StandardRepository
from ctr4ever.models.repository.standardsetrepository import StandardSetRepository
from ctr4ever.models.repository.standardtimerepository import StandardTimeRepository
from ctr4ever.models.repository.submissionrepository import SubmissionRepository
from ctr4ever.models.repository.trackrepository import TrackRepository
from ctr4ever.models.ruleset import Ruleset
from ctr4ever.models.standard import Standard
from ctr4ever.models.standardset import StandardSet
from ctr4ever.models.standardtime import StandardTime
from ctr4ever.models.submission import Submission
from ctr4ever.models.track import Track


class MockModelRepository(ModelRepository):
    """
    Unit testing functions which use repositories by using Mock() / MagicMock() is aids because sometimes you need dynamic
    return values for certain functions (like find_by()). While it creates overhead I prefer having a mock implementation
    of the model repository which can be used for unit testing.
    """

    def __init__(self):
        self._models = []
        self._id = 1
        self._model_class = self._get_model_class()

    def find_one(self, id):
        models = [model for model in self._models if model.id == id]

        if len(models) > 0:
            return models[0]

        return None

    def find_by(self, **kwargs):
        models = self._models

        for arg in kwargs:
            if kwargs[arg] is not None:
                if arg == 'limit' or arg == 'offset':
                    continue
                else:
                    models = [model for model in models if str(getattr(model, arg)) == str(kwargs[arg])]

        if 'offset' in kwargs:
            models = models[kwargs['offset']:]

        if 'limit' in kwargs:
            models = models[:kwargs['limit']]

        return models

    def count(self, **kwargs) -> int:
        return len(self.find_by(**kwargs))

    def create(self, **kwargs):
        model = self._model_class(**kwargs)
        model.id = self._id
        self._id += 1

        self._models.append(model)

        return model

    def update(self, **kwargs):
        if not 'id' in kwargs:
            raise ValueError('An id is required to update an entity')

        model = self.find_one(kwargs['id'])

        for attribute in kwargs:
            if kwargs[attribute] is not None:
                setattr(model, attribute, kwargs[attribute])

        return model

    @abstractmethod
    def _get_model_class(self):
        pass


class MockCategoryRepository(MockModelRepository, CategoryRepository):

    def find_by(self, name: str = None, limit: int = None, offset: int = None):
        return super().find_by(name=name, limit=limit, offset=offset)

    def create(self, name: str):
        return super().create(name=name)

    def count(self, name: str):
        return super().count(name=name)

    def update(self, id: int, name: str = None):
        super().update(id=id, name=name)

    def _get_model_class(self):
        return Category


class MockCharacterRepository(MockModelRepository, CharacterRepository):

    def find_by(self, name: str = None, limit: int = None, offset: int = None):
        return super().find_by(name=name, limit=limit, offset=offset)

    def count(self, name: str):
        return super().count(name=name)

    def create(self, name: str, engine_style_id: int, icon: str):
        return super().create(
            name=name,
            engine_style_id=engine_style_id,
            icon=icon
        )

    def update(self, id: int, name: str = None, engine_style_id: int = None, icon: str = None):
        super().update(
            id=id,
            name=name,
            engine_style_id=engine_style_id,
            icon=icon
        )

    def _get_model_class(self):
        return Character


class MockCountryRepository(MockModelRepository, CountryRepository):

    def find_by(self, name: str = None, limit: int = None, offset: int = None):
        return super().find_by(name=name, limit=limit, offset=offset)

    def count(self, name: str):
        return super().count(name=name)

    def create(self, name: str, flag: str):
        return super().create(name=name, flag=flag)

    def update(self, id: int, name: str = None, flag: str = None):
        super().update(id=id, name=name, flag=flag)

    def _get_model_class(self):
        return Country


class MockEngineStyleRepository(MockModelRepository, EngineStyleRepository):

    def find_by(self, name: str = None, limit: int = None, offset: int = None):
        return super().find_by(name=name, limit=limit, offset=offset)

    def count(self, name: str):
        return super().count(name=name)

    def create(self, name: str):
        return super().create(name=name)

    def update(self, id: int, name: str = None):
        super().update(id=id, name=name)

    def _get_model_class(self):
        return EngineStyle


class MockGameVersionRepository(MockModelRepository, GameVersionRepository):

    def find_by(self, name: str = None, limit: int = None, offset: int = None):
        return super().find_by(name=name, limit=limit, offset=offset)

    def count(self, name: str):
        return super().count(name=name)

    def create(self, name: str, icon: str):
        return super().create(name=name, icon=icon)

    def update(self, id: int, name: str = None, icon: str = None):
        super().update(id=id, name=name, icon=icon)

    def _get_model_class(self):
        return GameVersion


class MockPlatformRepository(MockModelRepository, PlatformRepository):

    def find_by(self, name: str = None, limit: int = None, offset: int = None):
        return super().find_by(name=name, limit=limit, offset=offset)

    def count(self, name: str):
        return super().count(name=name)

    def create(self, name: str):
        return super().create(name=name)

    def update(self, id: int, name: str = None):
        super().update(id=id, name=name)

    def _get_model_class(self):
        return Platform


class MockPlayerRepository(MockModelRepository, PlayerRepository):

    def find_by(
            self,
            country_id: int = None,
            name: str = None,
            email: str = None,
            active: bool = None,
            limit: int = None,
            offset: int = None
    ):
        return super().find_by(country_id=country_id, name=name, email=email, active=active, limit=limit, offset=offset)

    def count(
            self,
            country_id: int = None,
            name: str = None,
            email: str = None,
            active: bool = None
    ):
        return super().count(country_id=country_id, name=name, email=email, active=active)

    def create(self, country_id: int, name: str, email: str, password: str, salt: str, active: bool, created: datetime) -> Player:
        return super().create(
            country_id=country_id,
            name=name,
            email=email,
            password=password,
            salt=salt,
            active=active,
            created=created
        )

    def update(
            self,
            id: int,
            country_id: int = None,
            name: str = None,
            email: str = None,
            password: str = None,
            salt: str = None,
            active: bool = None
    ):
        super().update(
            id=id,
            country_id=country_id,
            name=name,
            email=email,
            password=password,
            salt=salt,
            active=active
        )

    def _get_model_class(self):
        return Player


class MockRulesetRepository(MockModelRepository, RulesetRepository):

    def find_by(self, name: str = None, limit: int = None, offset: int = None):
        return super().find_by(name=name, limit=limit, offset=offset)

    def count(self, name: str):
        return super().count(name=name)

    def create(self, name: str):
        return super().create(name=name)

    def update(self, id: int, name: str = None):
        super().update(id=id, name=name)

    def _get_model_class(self):
        return Ruleset


class MockStandardRepository(MockModelRepository, StandardRepository):

    def find_by(self, name: str = None, standard_set_id: int = None, limit: int = None, offset: int = None):
        return super().find_by(name=name, standard_set_id=standard_set_id, limit=limit, offset=offset)

    def count(self, name: str = None, standard_set_id: int = None):
        return super().count(name=name, standard_set_id=standard_set_id)

    def create(self, name: str, standard_set_id: int):
        return super().create(name=name, standard_set_id=standard_set_id)

    def update(self, id: int, name: str = None, standard_set_id: int = None):
        super().update(id=id, name=name, standard_set_id=standard_set_id)

    def _get_model_class(self):
        return Standard


class MockStandardSetRepository(MockModelRepository, StandardSetRepository):

    def find_by(self, name: str = None, limit: int = None, offset: int = None):
        return super().find_by(name=name, limit=limit, offset=offset)

    def count(self, name: str):
        return super().count(name=name)

    def create(self, name: str):
        return super().create(name=name)

    def update(self, id: int, name: str = None):
        super().update(id=id, name=name)

    def _get_model_class(self):
        return StandardSet


class MockStandardTimeRepository(MockModelRepository, StandardTimeRepository):

    def find_by(
            self,
            standard_id: int = None,
            track_id: int = None,
            category_id: int = None,
            limit: int = None,
            offset: int = None
    ):
        return super().find_by(
            standard_id=standard_id,
            track_id=track_id,
            category_id=category_id,
            limit=limit,
            offset=offset
        )

    def count(
            self,
            standard_id: int = None,
            track_id: int = None,
            category_id: int = None
    ):
        return super().count(
            standard_id=standard_id,
            track_id=track_id,
            category_id=category_id
        )

    def create(
            self,
            standard_id: int,
            track_id: int,
            category_id: int,
            time: float,
            numeric_value: int
    ) -> StandardTime:
        return super().create(
            standard_id=standard_id,
            track_id=track_id,
            category_id=category_id,
            time=time,
            numeric_value=numeric_value
        )

    def update(
            self,
            id: int,
            standard_id: int = None,
            track_id: int = None,
            category_id: int = None,
            time: float = None,
            numeric_value: int = None
    ) -> None:
        super().update(
            id=id,
            standard_id=standard_id,
            track_id=track_id,
            category_id=category_id,
            time=time,
            numeric_value=numeric_value
        )

    def _get_model_class(self) -> type:
        return StandardTime

class MockSubmissionRepository(MockModelRepository, SubmissionRepository):

    def find_by(
            self,
            player_id: int = None,
            track_id: int = None,
            category_id: int = None,
            character_id: int = None,
            game_version_id: int = None,
            ruleset_id: int = None,
            platform_id: int = None,
            limit: int = None,
            offset: int = None
    ):
        return super().find_by(
            player_id=player_id,
            track_id=track_id,
            category_id=category_id,
            character_id=character_id,
            game_version_id=game_version_id,
            ruleset_id=ruleset_id,
            platform_id=platform_id,
            limit=limit,
            offset=offset
        )

    def count(
            self,
            player_id: int = None,
            track_id: int = None,
            category_id: int = None,
            character_id: int = None,
            game_version_id: int = None,
            ruleset_id: int = None,
            platform_id: int = None
    ) -> int:
        return super().count(
            player_id=player_id,
            track_id=track_id,
            category_id=category_id,
            character_id=character_id,
            game_version_id=game_version_id,
            ruleset_id=ruleset_id,
            platform_id=platform_id
        )

    def create(
            self,
            player_id: int,
            track_id: int,
            category_id: int,
            character_id: int,
            game_version_id: int,
            ruleset_id: int,
            platform_id: int,
            time: float,
            date: datetime,
            video: str
    ) -> Submission:
        return super().create(
            player_id=player_id,
            track_id=track_id,
            category_id=category_id,
            character_id=character_id,
            game_version_id=game_version_id,
            ruleset_id=ruleset_id,
            platform_id=platform_id,
            time=time,
            date=date,
            video=video
        )

    def update(
            self,
            id: int,
            player_id: int = None,
            track_id: int = None,
            category_id: int = None,
            character_id: int = None,
            game_version_id: int = None,
            ruleset_id: int = None,
            platform_id: int = None,
            time: float = None,
            date: datetime = None,
            video: str = None
    ) -> None:
        super().update(
            id=id,
            player_id=player_id,
            track_id=track_id,
            category_id=category_id,
            character_id=character_id,
            game_version_id=game_version_id,
            ruleset_id=ruleset_id,
            platform_id=platform_id,
            time=time,
            date=date,
            video=video
        )

    def _get_model_class(self) -> type:
        return Submission

class MockTrackRepository(MockModelRepository, TrackRepository):

    def find_by(self, name: str = None, limit: int = None, offset: int = None):
        return super().find_by(name=name, limit=limit, offset=offset)

    def count(self, name: str):
        return super().count(name=name)

    def create(self, name: str):
        return super().create(name=name)

    def update(self, id: int, name: str = None):
        super().update(id=id, name=name)

    def _get_model_class(self):
        return Track
