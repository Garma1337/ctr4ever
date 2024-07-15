# coding=utf-8

from ctr4ever.rest.endpoint.authenticateplayer import AuthenticatePlayer
from ctr4ever.rest.endpoint.createsubmission import CreateSubmission
from ctr4ever.rest.endpoint.findcategories import FindCategories
from ctr4ever.rest.endpoint.findcharacters import FindCharacters
from ctr4ever.rest.endpoint.findenginestyles import FindEngineStyles
from ctr4ever.rest.endpoint.findgameversions import FindGameVersions
from ctr4ever.rest.endpoint.findplayers import FindPlayers
from ctr4ever.rest.endpoint.findrulesets import FindRulesets
from ctr4ever.rest.endpoint.findsubmissions import FindSubmissions
from ctr4ever.rest.endpoint.findtracks import FindTracks
from ctr4ever.rest.endpoint.loginplayer import LoginPlayer
from ctr4ever.rest.endpoint.registerplayer import RegisterPlayer

routes = {
    'authenticatePlayer': AuthenticatePlayer,
    'registerPlayer': RegisterPlayer,
    'loginPlayer': LoginPlayer,
    'characters': FindCharacters,
    'categories': FindCategories,
    'engineStyles': FindEngineStyles,
    'gameVersions': FindGameVersions,
    'players': FindPlayers,
    'rulesets': FindRulesets,
    'submissions': FindSubmissions,
    'tracks': FindTracks,
    'createSubmission': CreateSubmission
}
