# coding=utf-8

import click
from flask import Blueprint

from ctr4ever.container import container
from ctr4ever.services.installer.categoryinstaller import CategoryInstaller
from ctr4ever.services.installer.characterinstaller import CharacterInstaller
from ctr4ever.services.installer.countryinstaller import CountryInstaller
from ctr4ever.services.installer.enginestyleinstaller import EngineStyleInstaller
from ctr4ever.services.installer.gameversioninstaller import GameVersionInstaller
from ctr4ever.services.installer.platforminstaller import PlatformInstaller
from ctr4ever.services.installer.rulesetinstaller import RulesetInstaller
from ctr4ever.services.installer.trackinstaller import TrackInstaller

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

@installer.cli.command('countries')
@click.option('--filename', default=None, help='File to read countries from.')
def countries(filename: str):
    if not filename:
        click.echo('You need to specify a file name.')
        return

    country_installer: CountryInstaller = container.get('services.installer.country')

    try:
        country_installer.install(filename)
        click.echo('Successfully created countries.')
    except Exception as e:
        click.echo(f'Failed to set up countries: {e}')

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

@installer.cli.command('platforms')
@click.option('--filename', default=None, help='File to read platforms from.')
def platforms(filename: str):
    if not filename:
        click.echo('You need to specify a file name.')
        return

    platform_installer: PlatformInstaller = container.get('services.installer.platform')

    try:
        platform_installer.install(filename)
        click.echo('Successfully created platforms.')
    except Exception as e:
        click.echo(f'Failed to set up platforms: {e}')

@installer.cli.command('rulesets')
@click.option('--filename', default=None, help='File to read rulesets from.')
def rulesets(filename: str):
    if not filename:
        click.echo('You need to specify a file name.')
        return

    ruleset_installer: RulesetInstaller = container.get('services.installer.ruleset')

    try:
        ruleset_installer.install(filename)
        click.echo('Successfully created rulesets.')
    except Exception as e:
        click.echo(f'Failed to set up rulesets: {e}')

@installer.cli.command('tracks')
@click.option('--filename', default=None, help='File to read tracks from.')
def tracks(filename: str):
    if not filename:
        click.echo('You need to specify a file name.')
        return

    track_installer: TrackInstaller = container.get('services.installer.track')

    try:
        track_installer.install(filename)
        click.echo('Successfully created tracks.')
    except Exception as e:
        click.echo(f'Failed to set up tracks: {e}')
