class ProductDao:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def get_product_list(self, conn):
        pass

    def get_product_detail(self, conn, product_code):
        pass
