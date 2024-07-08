# coding=utf-8

import json
import os.path

import click
from flask import Blueprint

from ctr4ever.container import container
from ctr4ever.models.repository.characterrepository import CharacterRepository
from ctr4ever.models.repository.enginestylerepository import EngineStyleRepository

md: Blueprint = Blueprint('md', __name__)

@md.cli.command('upsert-characters')
@click.command()
@click.option('--file', help='JSON file to read character data from')
def upsert_characters(file: str):
    if not os.path.exists(file):
        click.echo(f'File "{file}" does not exist.')

    with open(file) as fp:
        characters = json.loads(fp.read())

        character_repository: CharacterRepository = container.get('repository.character_repository')
        engine_repository: EngineStyleRepository = container.get('repository.engine_style_repository')

        for character_data in characters:
            rows = engine_repository.find_by(name=character_data['engine'])

            if len(rows) <= 0:
                raise Exception(f'No engine {character_data['engine']} exists')

            engine = rows[0]

            character_repository.create(
                character_data['name'],
                engine.id,
                character_data['icon']
            )

        click.echo('Successfully created characters.')

@md.cli.command('create_tracks')
@click.command()
def create_tracks():
    tracks = []
    track_repository = container.get('repository.track_repository')

    for track in tracks:
        track_repository.create(track['name'])

    click.echo('Successfully created tracks.')

@md.cli.command('create_game_versions')
@click.command()
def create_game_versions():
    game_versions = []
    game_version_repository = container.get('repository.game_version_repository')

    for game_version in game_versions:
        game_version_repository.create(name=game_version['name'])

    click.echo('Successfully created game versions.')

@md.cli.command('create_categories')
@click.command()
def create_categories():
    categories = []
    category_repository = container.get('repository.category_repository')

    for category in categories:
        category_repository.create(category['name'])

    click.echo('Successfully created categories.')

@md.cli.command('create_countries')
@click.command()
def create_countries():
    countries = []
    country_repository = container.get('repository.country_repository')

    for country in countries:
        country_repository.create(country['name'])

    click.echo('Successfully created countries.')
