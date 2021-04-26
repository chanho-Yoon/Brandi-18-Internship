from flask import request, jsonify, g
from flask.views import MethodView
from flask_request_validator import validate_params, Param, GET, Datetime, ValidRequest

from connection import get_connection

from utils.decorator import LoginRequired

                            
#메인 - 홈 카테고리
class ProductListView(MethodView):
    def __init__(self, service):
        self.service = service
            pass

#상품상세
class ProductDetailView(MethodView):
    def __init__(self, service):
        self.service = service
            pass
    
