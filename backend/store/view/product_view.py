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
        """서비스 페이지의 상품 상세 정보 출력

        서비스 메인페이지에서 상품을 클릭했을 때 해당 상품 아이디를 받아 상세 정보를 출력한다.

        Args:
            product_id (int): 상품 아이디 

        Returns:
            [dict]: 해당 상품의 상세정보, 상품이 가진 색상 전체, 같은 셀러의 다른 상품을 전달
        """
        conn = None
        try:
            conn = get_connection()
            params = valid.get_path_params()
            
            return get_response(self.service.get_product_detail(conn, params))

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