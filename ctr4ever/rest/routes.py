# coding=utf-8

from ctr4ever.rest.endpoint.findcategories import FindCategories
from ctr4ever.rest.endpoint.findgameversions import FindGameVersions
from ctr4ever.rest.endpoint.findplayers import FindPlayers
from ctr4ever.rest.endpoint.findrulesets import FindRulesets
from ctr4ever.rest.endpoint.findsubmissions import FindSubmissions

routes = {
    'categories': FindCategories,
    'gameVersions': FindGameVersions,
    'players': FindPlayers,
    'rulesets' : FindRulesets,
    'submissions': FindSubmissions
}
