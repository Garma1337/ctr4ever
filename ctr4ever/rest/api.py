# coding=utf-8

from flask import Blueprint, request, current_app

from ctr4ever.rest.requestdispatcher import RequestDispatcher
from ctr4ever.rest.routes import routes
from ctr4ever.container import container

rest_api: Blueprint = Blueprint('api', __name__)

@rest_api.route('/api/<path:route>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def run(route):
    request_dispatcher: RequestDispatcher = RequestDispatcher(container, current_app.config)

    response = request_dispatcher.dispatch_request(
        routes,
        route,
        request
    )

    return response.get_data(), response.get_status_code()
