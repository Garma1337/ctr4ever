# coding=utf-8

from flask import Blueprint, request
from flask_cors import cross_origin
from flask_jwt_extended import verify_jwt_in_request

from ctr4ever.container import container
from ctr4ever.rest.requestdispatcher import RequestDispatcher

rest_api: Blueprint = Blueprint('api', __name__)

@rest_api.route('/api/<path:route>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@cross_origin()
def run(route):
    verify_jwt_in_request(optional=True)

    request_dispatcher: RequestDispatcher = container.get('api.request_dispatcher')

    response = request_dispatcher.dispatch_request(
        route,
        request
    )

    return response.get_data(), response.get_status_code()
