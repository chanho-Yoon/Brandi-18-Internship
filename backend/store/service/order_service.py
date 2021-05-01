from admin.model import OrderDao

from utils.response import error_response
from utils.custom_exception import DataNotExists, StartDateFail
from utils.constant import PURCHASE_COMPLETE, CANCEL_COMPLETE, REFUND_COMPLETE

import traceback
from datetime import timedelta, date

class OrderService:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance                      

    def __init__(self):
        self.order_dao = OrderDao()
    