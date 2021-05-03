from model import ProductDao
from datetime import timedelta, datetime
from utils.custom_exception import StartDateFail, NoMoreDataError
from io import BytesIO


class ProductService:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.product_dao = ProductDao()

    def get_product_list(self,conn, dc_params):
        """ 메인 페이지에 출력되는 상품정보

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

         # 첫 화면 상품갯수 설정 및 더보기 기능 offset 설정
        if dc_params['page']==1:
           dc_params['limit']=2 
        else:
           dc_params['offset'] = (dc_params['page'] - 1) * 1 + 1

        # 상품정보 리스트
        product_info_list = self.product_dao.get_product_list(conn, dc_params)
        
        # 불러올 상품 정보가 없는 경우
        if len(product_info_list) == 0:
            raise  NoMoreDataError("상품 정보를 가져올 수 없습니다.")

        # 할인기간 외 할인률 및 할인가 미표시
        for  product_info in  product_info_list:
            if not (product_info['discount_start'] <= datetime.now() and datetime.now() <= product_info['discount_end']):
                product_info['discount_rate'] = None
                product_info['price_discounted'] = None
        
        return product_info_list