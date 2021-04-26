from admin.model import ProductDao

class ProductService:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.product_dao = ProductDao()
    
    # 상품 리스트 가져오기
    def get_product_list(self, conn):
        return self.product_dao.get_product_list(conn)
    
    # 상품 상세 가져오기
    def get_product_detail(self, conn, product_code):
        return self.product_dao.get_product_detail(conn, product_code)