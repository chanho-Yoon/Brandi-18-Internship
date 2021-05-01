from flask.views import MethodView
from flask import request, jsonify
from flask_request_validator import Param, Pattern, JSON, validate_params, ValidRequest
from flask_request_validator.error_formatter import demo_error_formatter
from flask_request_validator.exceptions import InvalidRequestError, InvalidHeadersError, RuleError

from utils.custom_exception import DatabaseCloseFail
from utils.response import post_response

from connection import get_connection
from utils.decorator import LoginRequired



class SignUpView(MethodView):
    def __init__(self, service):
        self.service = service

class SignInView(MethodView):
    def __init__(self, service):
        self.service = service
        
class SignInSocialView(MethodView):
    def __init__(self, service):
        self.service = service
                            
                            