from model import ProductDao
from datetime import timedelta, datetime
from utils.custom_exception import StartDateFail
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
            dc_params : params를 deepcopy한 객체
        """
         # 더보기 기능 offset 설정
        if dc_params['page']==1:
           dc_params['limit']=2 
        else:
           dc_params['offset'] = (dc_params['page'] - 1) * 1 + 1

        # 상품정보 리스트
        product_info_list = self.product_dao.get_product_list(conn, dc_params)
        
        # 할인기간 외 할인률 및 할인가 미표시
        for  product_info in  product_info_list:
            if not (product_info['discount_start'] <= datetime.now() and datetime.now() <= product_info['discount_end']):
                product_info['discount_rate'] = None
                product_info['price_discounted'] = None
            
        return product_info_list