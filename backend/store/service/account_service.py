import bcrypt, jwt
from config import SECRET_KEY
from store.model import AccountDao
from utils.custom_exception import SignUpFail, SignInError, TokenCreateError

class AccountService:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.account_dao = AccountDao()
        
    def set_password_hash(self, params):
        params['password'] = bcrypt.hashpw(
            params['password'].encode('UTF-8'),
            bcrypt.gensalt()
        ).decode('UTF-8')
    
    def create_token(self, info):
        try:
            token = jwt.encode({"account_id": info['account_id']},
                                SECRET_KEY,
                                algorithm="HS256")
        except Exception as e:
            raise TokenCreateError("뜻하지 않은 에러가 발생했습니다. 다시 시도 해주세요.", "create_token error")
        
        return token
        
    def check_hash_password(self, conn, info, params):
        """ 로그인 hash password 체크하는 함수
        hash password 체크 후 account_type_id, accessToken값을 return하는 함수
        social 여부에 따라 각기 다른 로직이 실행되도록 조건문을 걸어뒀음. 소셜 로그인은 패스워드가 없기 때문
        
        Args:
            conn (class): DB 클래스
            info (dict): post_account_login or post_master_login에서 가져온 계정 정보
            params (dict): BODY에서 넘어온 master or seller 정보
        Returns:
            [dict]: account_type_id , accessToken
        """
        if params["social"] == "user" or params["social"] == "master":
            if not info or not bcrypt.checkpw(params['password'].encode('utf-8'), info['password'].encode('utf-8')):
                raise SignInError("정확한 아이디, 비밀번호를 입력해주세요", "post_master_login error")
            account_type_id = self.account_dao.get_account_type_id(conn, info)
            token = self.create_token(info)
            
        elif params["social"] == "google":
            account_type_id = self.account_dao.get_account_type_id(conn, info)
            token = self.create_token(info)
        return {
            "account_type_id" : account_type_id['account_type_id'],
            "accessToken" : token
        }
    # -------------------------------------------------------------------------------------------
    # user 회원가입
    def post_user_signup(self, conn, params):
        # id 중복확인
        checkid = self.account_dao.get_userid(conn, params)
        if checkid:
            raise SignUpFail("중복된 아이디 입니다.", "already_exist_id")

        # email 중복확인
        check_email = self.account_dao.get_email(conn, params)
        if check_email:
            raise SignUpFail("중복된 이메일 입니다.", "already_exist_email")
        
        # 휴대폰 중복확인
        check_phone = self.account_dao.get_phone(conn, params)
        if check_phone:
            raise SignUpFail("중복된 휴대폰 번호 입니다.", "aready_exist_phone")
        
        # password hash
        self.set_password_hash(params)
        
        # account_type (user = 3)
        params['account_type_id'] = 3
        # account 생성
        get_account_id = self.account_dao.create_account(conn, params)
        if not get_account_id:
            raise SignUpFail("아이디를 생성하는데 오류가 발생했습니다.","create_account error")
        params['account_id'] = get_account_id
        
        # user 생성
        get_user_id = self.account_dao.create_user_signup(conn, params)
        if not get_user_id:
            raise SignUpFail("아이디를 생성하는데 오류가 발생했습니다.","create_user_signup error")
        params['user_id'] = get_user_id
        
        # user history 생성
        get_user_history_id = self.account_dao.create_user_history(conn, params)
        if not get_user_history_id:
            raise SignUpFail("아이디를 생성하는데 오류가 발생했습니다.", "create_user_history error")
    
    # user 로그인
    def post_user_login(self, conn, params):
        user_info = self.account_dao.post_user_login(conn, params)
        result = self.check_hash_password(conn, user_info, params)
        return result
    
    def post_user_social_login(self, conn, params):
        # 먼저 account_id에 가입되어 있는 정보가 있는지 확인
        checkid = self.account_dao.get_social_user_identification(conn, params)
        # 로그인 하는데 아이디가 있다면 회원가입 처리 로직 실행
        if not checkid :
            # account 생성
            get_account_id = self.account_dao.create_account(conn, params)
            if not get_account_id:
                raise SignUpFail("아이디를 생성하는데 오류가 발생했습니다.","post_user_socail_login, get_account_id error")
            params['account_id'] = get_account_id
            # user 생성
            get_user_id = self.account_dao.create_user_signup(conn, params)
            if not get_user_id:
                raise SignUpFail("아이디를 생성하는데 오류가 발생했습니다.","post_user_social_login, get_user_id error")
            params['user_id'] = get_user_id

            # user history 생성
            get_user_history_id = self.account_dao.create_user_history(conn, params)
            if not get_user_history_id:
                raise SignUpFail("아이디를 생성하는데 오류가 발생했습니다.", "post_user_social_login, get_user_history_id error")
            
            # social user 생성
            get_social_user_id = self.account_dao.create_social_user_signup(conn, params)
            if not get_social_user_id:
                raise SignUpFail("아이디를 생성하는데 오류가 발생했습니다.","post_user_social_login, get_social_user_id error")
            
            user_info = self.account_dao.post_user_login(conn, params)
            result = self.check_hash_password(conn, user_info, params)
            
            return result
        # 아이디가 이미 존재한다면 로그인 처리
        else :
            user_info = self.account_dao.post_user_login(conn, params)
            result = self.check_hash_password(conn, user_info, params)
            
            return result
    