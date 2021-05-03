import copy
from flask import request, jsonify, g, send_file
from flask.views import MethodView
from flask_request_validator import validate_params, Param, GET, Datetime, ValidRequest, CompositeRule, Min, Max, Enum, JsonParam, JSON, HEADER
from datetime import datetime
from connection import get_connection
from utils.response import get_response, post_response
from utils.custom_exception import IsInt, IsStr, IsFloat, IsRequired, DatabaseCloseFail
from flask_request_validator.exceptions import InvalidRequestError, RulesError
from utils.decorator import LoginRequired


class ProductView(MethodView):
    def __init__(self, service):
        self.service = service

    @validate_params(
        Param('page', GET, int, required=False, default=1, rules=[Min(1)]),
        Param('limit', GET, int, required=False, default=1),
        Param('offset', GET, int, required=False, default=0),
    )
       
    def get(self, valid: ValidRequest):
        """ 메인페이지
            최신등록된 상품순으로 출력
        Args:
            valid (dict): 대표이미지,상호,상품명,할인율,(할인)가격,원가격,판매량
        Returns:
            200: 상품 리스트 가져오기 성공
            500: Exception
        """
        try:
            params = valid.get_params()
            dc_params = copy.deepcopy(params)
            conn = get_connection()
            result = self.service.get_product_list(conn, dc_params)
            return get_response(result)

        finally:
            try:
                conn.close()
            except Exception as e:
                raise DatabaseCloseFail('서버에 알 수 없는 오류가 발생했습니다.')


class ProductDetailView(MethodView):
    def __init__(self, service):
        self.service = service

    # 상품 상세
    # @LoginRequired
    def get(self, product_code):
        conn = None
        try:
            conn = get_connection()
            if conn:
                result = self.service.get_product_detail(conn, product_code)

            return jsonify(result), 200

        finally:
            conn.close()