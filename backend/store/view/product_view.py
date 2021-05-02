from flask import request, jsonify, g, send_file
from flask.views import MethodView
from flask_request_validator import validate_params, PATH, Param, GET, Datetime, ValidRequest, CompositeRule, Min, Max, Enum, JsonParam, JSON, HEADER
from datetime import datetime
from connection import get_connection
from utils.response import get_response, post_response
from utils.decorator import LoginRequired, LoginCheck
from utils.custom_exception import IsInt, IsStr, IsFloat, IsRequired, DatabaseCloseFail
from flask_request_validator.exceptions import InvalidRequestError, RulesError
import xlwt

from utils.decorator import LoginRequired


class ProductView(MethodView):
    def __init__(self, service):
        self.service = service

class ProductDetailView(MethodView):
    def __init__(self, service):
        self.service = service

    @validate_params(
        Param('product_id', PATH, int)
    )
    def get(self, valid: ValidRequest, product_id):
        conn = None
        try:
            conn = get_connection()
            params = valid.get_path_params()
            result = self.service.get_product_detail(conn, params)

            return get_response(result)

        finally:
            try:
                conn.close()
            except Exception as e:
                raise DatabaseCloseFail('서버에 알 수 없는 오류가 발생했습니다.')

class ProductOptionView(MethodView):
    def __init__(self, service):
        self.service = service
    
    @validate_params(
        Param('product_id', PATH, int),
        Param('color_id', PATH, int)
    )
    def get(self, valid:ValidRequest, product_id, color_id):
        conn = None
        try:
            conn = get_connection()
            params = valid.get_path_params()

            result = self.service.get_product_option(conn, params)

            return get_response(result)

        finally:
            try:
                conn.close()
            except Exception as e:
                raise DatabaseCloseFail('서버에 알 수 없는 오류가 발생했습니다.')

class ProductQuestionAnswerView(MethodView):
    def __init__(self, service):
        self.service = service
    
    @validate_params(
        Param('product_id', PATH, int),
        Param('page', GET, int, required=False, default=1, rules=[Min(1)]),
        Param('limit', GET, int, required=False, default=5, rules=CompositeRule(Min(5), Max(50)))
    )
    @LoginCheck('user')
    def get(self, valid:ValidRequest, product_id):
        conn = None
        try:
            conn = get_connection()
            params = valid.get_params()
            params['product_id'] = product_id

            return get_response(self.service.get_product_question_answer(conn, params))

        finally:
            try:
                conn.close()
            except Exception as e:
                raise DatabaseCloseFail('서버에 알 수 없는 오류가 발생했습니다.')