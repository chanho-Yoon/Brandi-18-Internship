from utils.response import error_response, get_response, post_response, post_response_with_return

from flask import request, jsonify, g
from flask.views import MethodView
from flask_request_validator import validate_params, Param, GET, ValidRequest, JsonParam, Min, Enum, Datetime

from connection import get_connection
from utils.response import error_response, get_response, post_response, post_response_with_return
from utils.custom_exception import DataNotExists, StartDateFail
from utils.decorator import LoginRequired


class OrderListView(MethodView):
    def __init__(self, service):
        self.service = service
        pass
    
class OrderView(MethodView):
    def __init__(self, service):
        self.service = service
        pass