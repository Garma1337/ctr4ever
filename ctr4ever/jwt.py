# coding=utf-8

from flask import Flask
from flask_jwt_extended import JWTManager

from ctr4ever.container import container
from ctr4ever.models.player import Player
from ctr4ever.models.repository.playerrepository import PlayerRepository

jwt = JWTManager()

def init_app(app: Flask):
    jwt.init_app(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user: Player):
        return user.to_dictionary()

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        player_repository: PlayerRepository = container.get('repository.player')
        identity = jwt_data['sub']
        return player_repository.find_one(identity['id'])