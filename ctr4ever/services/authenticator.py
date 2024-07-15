# coding=utf-8

from ctr4ever.models.player import Player
from ctr4ever.models.repository.countryrepository import CountryRepository
from ctr4ever.models.repository.playerrepository import PlayerRepository
from ctr4ever.services.passwordmanager import PasswordManager


class RegistrationError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class Authenticator(object):

    def __init__(
            self,
            password_manager: PasswordManager,
            country_repository: CountryRepository,
            player_repository: PlayerRepository
    ):
        self.password_manager = password_manager
        self.country_repository = country_repository
        self.player_repository = player_repository

    def authenticate_player(self, username: str, password: str) -> bool:
        players = self.player_repository.find_by(name=username)

        if len(players) <= 0:
            return False

        player = players[0]

        if not self.password_manager.check_password(password, player.password, player.salt):
            return False

        return True

    def login_player(self, username: str, password: str):
        pass

    def register_player(self, country_id: int, username: str, email: str, password: str) -> Player:
        country = self.country_repository.find_one(country_id)

        if not country:
            raise RegistrationError(f'No country with id "{country_id}" exists.')

        existing_players = self.player_repository.find_by(name=username)

        if len(existing_players) > 0:
            raise RegistrationError(f'A player with name "{username}" already exists.')

        existing_players = self.player_repository.find_by(email=email)

        if len(existing_players) > 0:
            raise RegistrationError(f'The e-mail address "{email}" is already in use.')

        if not self.password_manager.is_secure_password(password):
            raise RegistrationError('The provided password is not secure enough.')

        salt = self.password_manager.generate_salt()
        player = self.player_repository.create(country_id, username, email, password, salt, True)

        return player
