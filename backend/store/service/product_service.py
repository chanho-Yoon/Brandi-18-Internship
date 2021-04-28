# from model import ProductDao
# from datetime import timedelta, datetime
# from utils.custom_exception import StartDateFail
# import xlwt
# from io import BytesIO
# # from flask import send_file

class ProductService:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.product_dao = ProductDao()
  