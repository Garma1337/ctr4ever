# coding=utf-8

from ctr4ever.rest.endpoint.getgameversions import GetGameVersion
from ctr4ever.rest.endpoint.getplayer import GetPlayer

routes = {
    'player': GetPlayer,
    'gameVersion': GetGameVersion
}
