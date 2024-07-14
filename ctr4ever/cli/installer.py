# coding=utf-8

import click
from flask import Blueprint

from ctr4ever.container import container
from ctr4ever.services.installer.categoryinstaller import CategoryInstaller
from ctr4ever.services.installer.characterinstaller import CharacterInstaller
from ctr4ever.services.installer.enginestyleinstaller import EngineStyleInstaller
from ctr4ever.services.installer.gameversioninstaller import GameVersionInstaller

installer: Blueprint = Blueprint('installer', __name__)

@installer.cli.command('categories')
@click.option('--filename', default=None, help='File to read categories from.')
def categories(filename: str):
    if not filename:
        click.echo('You need to specify a file name.')
        return

    category_installer: CategoryInstaller = container.get('services.installer.category')

    try:
        category_installer.install(filename)
        click.echo('Successfully created categories.')
    except Exception as e:
        click.echo(f'Failed to set up categories: {e}')

@installer.cli.command('characters')
@click.option('--filename', default=None, help='File to read characters from.')
def characters(filename: str):
    if not filename:
        click.echo('You need to specify a file name.')
        return

    character_installer: CharacterInstaller = container.get('services.installer.character')

    try:
        character_installer.install(filename)
        click.echo('Successfully created characters.')
    except Exception as e:
        click.echo(f'Failed to set up characters: {e}')

@installer.cli.command('engine_styles')
@click.option('--filename', default=None, help='File to read engine styles from.')
def engine_styles(filename: str):
    if not filename:
        click.echo('You need to specify a file name.')
        return

    engine_style_installer: EngineStyleInstaller = container.get('services.installer.engine_style')

    try:
        engine_style_installer.install(filename)
        click.echo('Successfully created engine styles.')
    except Exception as e:
        click.echo(f'Failed to set up engine styles: {e}')

@installer.cli.command('game_versions')
@click.option('--filename', default=None, help='File to read game versions from.')
def game_versions(filename: str):
    if not filename:
        click.echo('You need to specify a file name.')
        return

    game_version_installer: GameVersionInstaller = container.get('services.installer.game_version')

    try:
        game_version_installer.install(filename)
        click.echo('Successfully created game versions.')
    except Exception as e:
        click.echo(f'Failed to set up game versions: {e}')
