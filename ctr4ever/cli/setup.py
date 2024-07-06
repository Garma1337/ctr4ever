# coding=utf-8

import click
from flask import Blueprint

from ctr4ever.container import container

setup: Blueprint = Blueprint('setup', __name__)

@setup.cli.command('create_characters')
@click.command()
def create_characters():
    characters = [
        {
            'name' : 'Crash',
            'icon' : 'crash.png'
        },
        {
            'name': 'Coco',
            'icon': 'coco.png'
        },
        {
            'name': 'Polar',
            'icon': 'polar.png'
        },
        {
            'name': 'Pura',
            'icon': 'pura.png'
        },
        {
            'name': 'Dingodile',
            'icon': 'dingodile.png'
        },
        {
            'name': 'Tiny',
            'icon': 'tiny.png'
        },
        {
            'name': 'Cortex',
            'icon': 'cortex.png'
        },
        {
            'name': 'N. Gin',
            'icon': 'ngin.png'
        },
        {
            'name': 'Ripper Roo',
            'icon': 'ripperroo.png'
        },
        {
            'name': 'Papu Papu',
            'icon': 'papu.png'
        },
        {
            'name': 'Komodo Joe',
            'icon': 'komodojoe.png'
        },
        {
            'name': 'Pinstripe',
            'icon': 'pinstripe.png'
        },
        {
            'name': 'N. Tropy',
            'icon': 'ntropy.png'
        },
        {
            'name': 'Fake Crash',
            'icon': 'fakecrash.png'
        },
        {
            'name': 'Fast Penta Penguin',
            'icon': 'penta.png'
        },
        {
            'name': 'Slow Penta Penguin',
            'icon': 'penta.png'
        },
    ]

    character_repository = container.get('repository.character_repository')

    for character_data in characters:
        character_repository.create(
            character_data['name'],
            character_data['icon']
        )

    click.echo('Successfully created characters.')

@setup.cli.command('create_tracks')
@click.command()
def create_tracks():
    tracks = [
        'Crash Cove',
        "Roo's Tubes",
        'Mystery Caves',
        'Sewer Speedway',
        'Coco Park',
        'Tiger Temple',
        "Papu's Pyramid",
        'Dingo Canyon',
        'Blizzard Bluff',
        'Dragon Mines',
        'Polar Pass',
        'Tiny Arena',
        'N. Gin Labs',
        'Cortex Castle',
        'Hot Air Skyway',
        'Oxide Station',
        'Slide Coliseum',
        'Turbo Track'
    ]

    track_repository = container.get('repository.track_repository')

    for track_name in tracks:
        track_repository.create(track_name)

    click.echo('Successfully created tracks.')

@setup.cli.command('create_game_versions')
@click.command()
def create_game_versions():
    game_versions = [
        'PAL',
        'NTSC-U',
        'NTSC-J'
    ]

    game_version_repository = container.get('repository.game_version_repository')

    for game_versions_name in game_versions:
        game_version_repository.create(name=game_versions_name)

    click.echo('Successfully created game versions.')

@setup.cli.command('create_categories')
@click.command()
def create_categories():
    categories = [
        'Course',
        'Lap',
        'SL',
        'Relic Race',
        'Course (Fast)',
        'Lap (Fast)',
        'Course (Accel)',
        'Lap (Accel)',
        'Course (Medium)',
        'Lap (Medium)',
        'Course (Slow)',
        'Lap (Slow)'
    ]

    category_repository = container.get('repository.category_repository')

    for category_name in categories:
        category_repository.create(category_name)

    click.echo('Successfully created categories.')

@setup.cli.command('create_countries')
@click.command()
def create_countries():
    countries = []
