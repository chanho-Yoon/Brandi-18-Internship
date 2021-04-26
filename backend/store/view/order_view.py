from flask import request, jsonify
from flask.views import MethodView
from flask_request_validator import validate_params, Param, GET, ValidRequest

from connection import get_connection

#주문 페이지
class OrderView(MethodView):
    def __init__(self, service):
        self.service = service
            pass
   
        