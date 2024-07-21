# coding=utf-8

from flask import Blueprint

web: Blueprint = Blueprint('web', __name__, static_folder='resources', static_url_path="/")

@web.route('/', defaults={'path': ''})
@web.route('/<path:path>')
def catch_all(path):
    return web.send_static_file('index.html')
