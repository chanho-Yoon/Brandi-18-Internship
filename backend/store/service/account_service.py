import bcrypt, jwt

from admin.model import AccountDao
from utils.custom_exception import SignUpFail

class AccountService:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.account_dao = AccountDao()
        pass
