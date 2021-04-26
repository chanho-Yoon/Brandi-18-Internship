from admin.model import OrderDao

class OrderService:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance                      

    def __init__(self):
        self.order_dao = OrderDao()
    
    # 주문 조회
    def get_order_list(self, conn, params):
        return self.order_dao.get_order_list(conn, params)
