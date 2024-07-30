# coding=utf-8

from ctr4ever.models.repository.countryrepository import CountryRepository
from ctr4ever.models.repository.playerrepository import PlayerRepository
from ctr4ever.services.passwordmanager import PasswordManager
from ctr4ever.services.validator.validator import Validator, ValidationError


class PlayerValidator(Validator):

    def __init__(
            self,
            country_repository: CountryRepository,
            player_repository: PlayerRepository,
            password_manager: PasswordManager
    ):
        self.country_repository = country_repository
        self.player_repository = player_repository
        self.password_manager = password_manager

    def validate_player(self, name: str, country_id: int, email: str, password: str):
        self.validate_name(name)
        self.validate_country(country_id)
        self.validate_email(email)
        self.validate_password(password)

    def validate_name(self, name: str):
        if not name:
            raise ValidationError('The player name cannot be empty.')

        existing_players = self.player_repository.find_by(name=name)

        if len(existing_players) > 0:
            raise ValidationError(f'A player with the name "{name}" already exists.')

    def validate_country(self, country_id: int):
        if not country_id:
            raise ValidationError('The player country cannot be empty.')

        country = self.country_repository.find_one(country_id)

        if not country:
            raise ValidationError(f'No country with the id "{country_id}" exists.')

    def validate_email(self, email: str):
        if not email:
            raise ValidationError('The player e-mail cannot be empty.')

        existing_players = self.player_repository.find_by(email=email)

        if len(existing_players) > 0:
            raise ValidationError(f'The e-mail address "{email}" is already in use.')

        if not '@' in email:
            raise ValidationError(f'"{email}" is not valid e-mail address.')

    def validate_password(self, password: str):
        if not self.password_manager.is_secure_password(password):
            raise ValidationError('The password is not secure enough.')

    def validate_id(self, player_id: int):
        if not player_id:
            raise ValidationError('The player id cannot be empty.')

        player = self.player_repository.find_one(player_id)

        if not player:
            raise ValidationError(f'No player with the id "{player_id}" exists.')
