# coding=utf-8

import click
from flask import Blueprint

from ctr4ever import db
from ctr4ever.services.faker import Faker

faker: Blueprint = Blueprint('faker', __name__)

@faker.cli.command('generate_users')
@click.command()
def generate_users():
    faker_service: Faker = Faker(db)
    faker_service.generate_fake_players()

    click.echo('Successfully created fake players.')
