from flask.views import MethodView
from flask import request, jsonify
from flask_request_validator import Param, Pattern, JSON, validate_params, ValidRequest
from flask_request_validator.error_formatter import demo_error_formatter
from flask_request_validator.exceptions import InvalidRequestError, InvalidHeadersError, RulesError

from utils.custom_exception import DatabaseCloseFail
from utils.response import post_response
from utils.decorator import LoginRequired
from connection import get_connection

class SignUpView(MethodView):
    def __init__(self, service):
        self.service = service
    
    @validate_params(
        Param('id', JSON, str, rules=[Pattern("^[a-z]+[a-z0-9]{4,19}$")], required=True),
        Param('email', JSON, str, rules=[Pattern('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')], required=True),
        Param('user_type_id', JSON, str, required=True),
        Param('password', JSON, str, rules=[Pattern('^[A-Za-z0-9@#$]{6,12}$')], required=True),
        Param('phone', JSON, str, required=True),
        Param('date_of_birth', JSON, str, required=False),
        Param('receiving_event_is_agreed', JSON, bool, required=False),
        Param('notifying_benefit_is_agreed', JSON, bool, required=False)
    )
    def post(self, valid: ValidRequest):
        conn = None
        try:
            body = valid.get_json()
            conn = get_connection()
            self.service.post_user_signup(conn, body)
            conn.commit()

            return post_response({"message": "success", "status_code" : 200}), 200
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            try:
                if conn:
                    conn.close()
            except Exception as e:
                raise DatabaseCloseFail('서버에 알 수 없는 오류가 발생했습니다.')

class SignInView(MethodView):
    def __init__(self, service):
        self.service = service
        
    @validate_params(
        Param('id', JSON, str, rules=[Pattern("^[a-z]+[a-z0-9@.]{4,19}$")], required=True),
        Param('password', JSON, str, rules=[Pattern('^[A-Za-z0-9@#$]{6,12}$')], required=True),
        Param('social', JSON, str, required=True)
    )
    def post(self, valid):
        conn = None
        try:
            body = valid.get_json()        
            conn = get_connection()

            result = self.service.post_user_login(conn, body)
            
            return post_response({
                        "message" : "success", 
                        "accessToken" : result['accessToken'],
                        "account_type_id" : result['account_type_id'],
                        "status_code" : 200
                        }), 200
        finally:
            try:
                if conn:
                    conn.close()
            except Exception as e:
                raise DatabaseCloseFail('서버에 알 수 없는 오류가 발생했습니다.')

class SignInSocialView(MethodView):
    def __init__(self, service):
        self.service = service
        
    @validate_params(
        Param('id', JSON, str, rules=[Pattern("[a-z0-9]{4,100}$")], required=True),
        Param('email', JSON, str, rules=[Pattern('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')], required=True),
        Param('account_type_id', JSON, str, required=True),
        Param('user_type_id', JSON, str, required=True),
        Param('social_type_id', JSON, str, required=True),
        Param("social", JSON, str, required=True),
        Param('receiving_event_is_agreed', JSON, bool, required=False),
        Param('notifying_benefit_is_agreed', JSON, bool, required=False)
    )
    def post(self, valid: ValidRequest):
        try:
            body = valid.get_json()
            conn = get_connection()
            result = self.service.post_user_social_login(conn, body)
            conn.commit()
    
            return post_response({
                        "message" : "success", 
                        "accessToken" : result['accessToken'],
                        "account_type_id" : result['account_type_id'],
                        "status_code" : 200
                        }), 200
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            try:
                if conn:
                    conn.close()
            except Exception as e:
                raise DatabaseCloseFail('서버에 알 수 없는 오류가 발생했습니다.')
    
        
    
    
    