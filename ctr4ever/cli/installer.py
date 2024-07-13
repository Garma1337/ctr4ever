# coding=utf-8

import click
from flask import Blueprint

from ctr4ever.container import container
from ctr4ever.services.installer.categoryinstaller import CategoryInstaller

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
