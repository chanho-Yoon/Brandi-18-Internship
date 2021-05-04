import copy, xlwt
from flask import g
from model import ProductDao
from datetime import timedelta, datetime
from utils.custom_exception import StartDateFail, DataNotExists
from io import BytesIO
# from flask import send_file



class ProductService:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.product_dao = ProductDao()

    def get_product_list(self,conn, params):
        """ 
        메인 페이지에 출력되는 상품정보

        Args:
            conn (pymysql.connections.Connection): DB 커넥션 객체
            dc_params : params의 deepcopy객체

        Returns:
            product_info_list = 
                "result": [{
                    "discount_end": 할인종료일,
                    "discount_rate": 할인율,
                    "discount_start": 할인 시작일,
                    "price_discounted": 할인적용가격,
                    "price_origin": 원 가격,
                    "product_id": 제품 id,
                    "product_img": 이미지 url,
                    "product_name": 상품명,
                    "product_sold": 상품 판매량,
                    "store_name": 점표명
                    }]
        """

        dc_params = copy.deepcopy(params)
        
        # 첫 화면 상품갯수 설정
        if dc_params['page']==1:
           dc_params['limit']=2 
        #  더보기 기능 offset 설정
        else:
           dc_params['offset'] = (dc_params['page'] - 1) * 1 + 1

        # 상품정보 리스트
        product_info_list = self.product_dao.get_product_list(conn, dc_params)
        
        #불러올 상품 정보가 없는 경우
        if len(product_info_list) == 0:
            raise  DataLoadError("상품 정보를 가져올 수 없습니다.")

        return product_info_list
    
    def get_product_detail(self, conn, params):
        # 상품 상세, 상품이미지, 상품옵션, 셀러의 다른상품 가져오기
        product_detail, product_image, product_option, other_product = self.product_dao.get_product_detail(conn, params)
    
        result = {
            # 상품 아이디
            'product_id' : product_detail['product_id'],
            # 셀러 아이디
            'seller_id' : product_detail['seller_id'],
            # 셀러 한국 이름
            'seller_korean_name' : product_detail['seller_korean_name'],
            # 상품 제목
            'product_title' : product_detail['title'],
            # 상품 가격
            'price' : product_detail['price'],
            # 상품 할인율
            'discount_rate' : product_detail['discount_rate'],
            # 상품 할인가격
            'discount_price' : product_detail['price'] - product_detail['price'] * product_detail['discount_rate'],
            # 상품 상세정보
            'detail_description' : product_detail['detail_description'],
            # 상품의 이미지, 대표이미지 여부
            'images' : [
                {
                    'image_url' : image['image_url'],
                    'is_represent' : image['is_represent']
                }
            for image in product_image],
            # 상품의 옵션 리스트
            'options' : [
                {
                    'id' : option['option_id'],
                    'size_id' : option['size_id'],
                    'color_id' : option['color_id'],
                    'size_name' : option['size_name'],
                    'color_name' : option['color_name'],
                    'option_price' : option['price'],
                    'stock' : option['stock']
                }
                for option in product_option
            ],
            # 셀러의 다른 상품 최신순 5개
            'other_product' : [
                {   
                    'seller_korean_name' : product_detail['seller_korean_name'],
                    'image_url' : other['image_url'],
                    'title' : other['title'],
                    'price' : other['price'],
                    'discount_rate' : other['discount_rate'],
                    'discount_price' : other['price'] - other['price'] * other['discount_rate'],
                    'product_id' : other['product_id']
                }
                for other in other_product
            ]
        }
        return result
    
    def get_product_question_answer(self, conn, params):
        # 요청으로 들어온 값을 복합객체, 내용 복사
        request_data = copy.deepcopy(params)
        
        # 페이지네이션 위한 OFFSET 설정
        request_data['offset'] = (request_data['page'] - 1) * request_data['limit']

        # 데이터베이스에 상품 존재하는지 확인
        exists = self.product_dao.check_product_exists(conn, params)
        if not exists['count']:
            raise DataNotExists('상품이 존재하지 않습니다.', 'product does not exist')

        # 데이터베이스에 질문이 없다면 return
        total_count_question = self.product_dao.get_total_count_question(conn, request_data)
        if total_count_question['total_count'] == 0:
            return total_count_question

        # 질문 정보, 답변 정보
        question_result, answer_result = self.product_dao.get_product_question_answer(conn, request_data)

        result = {
            # 질문 총 갯수
            'total_count' : total_count_question['total_count'],
            # 질문 정보
            'questions' : [
                {   
                    # 질문 아이디
                    'question_id' : question['question_id'],
                    # 질문 타입 정보
                    'question_type_name' : question['question_type_name'],
                    # 질문 타입 아이디
                    'question_type_id' : question['question_type_id'],
                    # 질문 답변여부
                    'question_answer_status' : question['question_answer_status'],
                    # 질문 내용
                    'question_content' : question['question_content'],
                    # 질문 등록 유저 identification
                    'user_identification' : question['question_user_identification'],
                    # 질문 등록 유저 아이디
                    'user_id' : question['question_user_id'],
                    # 질문 등록일
                    'question_upload_date' : question['question_upload_date'],
                    # 질문 공개 여부
                    'question_secret_status' : question['question_secret_status'] if question['account_id'] != g.account_id else 0,
                    # 답변 정보
                    'answer' : [
                        {   
                            # 답변 아이디
                            'answer_id' : answer['answer_id'],
                            # 답변한 질문 아이디
                            'answer_question_id' : answer['answer_question_id'],
                            # 답변 내용
                            'answer_content' : answer['answer_content'],
                            # 답변 등록일
                            'answer_upload_date' : answer['answer_upload_date'],
                            # 답변 유저 identification
                            'answer_identification' : answer['name'],
                            # 답변 유저 아이디
                            'answer_account_id' : answer['account_id']
                        }
                        for answer in answer_result if answer['answer_question_id'] == question['question_id']
                    ]
                }
                for question in question_result
            ]
        }
        return result
