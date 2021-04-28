# from flask import request, jsonify, g, send_file
# from flask.views import MethodView
# from flask_request_validator import validate_params, Param, GET, Datetime, ValidRequest, CompositeRule, Min, Max, Enum, JsonParam, JSON, HEADER
# from datetime import datetime
# from connection import get_connection
# from utils.response import get_response, post_response
# from utils.custom_exception import IsInt, IsStr, IsFloat, IsRequired, DatabaseCloseFail
# from flask_request_validator.exceptions import InvalidRequestError, RulesError
# import xlwt

# from utils.decorator import LoginRequired


class ProductView(MethodView):
    def __init__(self, service):
        self.service = service

class ProductDetailView(MethodView):
    def __init__(self, service):
        self.service = service
