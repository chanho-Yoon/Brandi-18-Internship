from flask.views import MethodView
from flask import request, jsonify
from flask_request_validator import Param, Pattern, JSON, validate_params, ValidRequest
from flask_request_validator.error_formatter import demo_error_formatter
from flask_request_validator.exceptions import InvalidRequestError, InvalidHeadersError, RuleError

#from utils.custom_exception import DatabaseCloseFail, DatabaseConnectFail

from connection import get_connection
from utils.decorator import LoginRequired

#회원가입
class SignUpView(MethodView):
       def __init__(self, service):
              self.service = service
              pass
       
#로그인
class SignInView(MethodView):\
       def __init__(self, service):
              self.service = service
              pass
#소설로그인
class SocialSignInView(MethodView):
       def __init__(self, service):
              self.service = service
              pass

#마이페이지-추가구현사항
class MyPageView(MethodView):
       def __init__(self, service):
              self.service = service
              pass