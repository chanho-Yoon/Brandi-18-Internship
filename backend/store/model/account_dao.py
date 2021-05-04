class AccountDao:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def get_userid(self, conn, params):
        """user id 중복 확인 함수

        Args:
            conn (class): DB 클래스
            params (dict): body에서 넘어온 user 회원가입 정보
        """
        sql = """
            SELECT 
                *
            FROM
                users
            WHERE
                user_identification = %(id)s
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
    
    def get_account_type_id(self, conn, params):
        """account_type_id를 가져오는 함수

        Args:
            conn (class): DB 클래스
            params (dict): seller id값을 이용해서 가져온 seller_info 정보
        """
        sql = """
            SELECT
                account_type_id
            FROM
                account
            WHERE
                id = %(account_id)s
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
    
    def get_email(self, conn, params):
        """user email 중복 확인하는 함수

        Args:
            conn (class): DB 클래스
            params (dict): BODY에서 넘어온 user 회원가입 정보
        """
        sql = """
            SELECT
                *
            FROM
                users
            WHERE
                email =  %(email)s
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
    
    def get_phone(self, conn, params):
        """user phone 중복 확인하는 함수

        Args:
            conn (class): DB 클래스
            params (dict): BODY에서 넘어온 user 회원가입 정보
        """
        sql = """
            SELECT
                *
            FROM
                users
            WHERE
                phone = %(phone)s
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
        
    def create_account(self, conn, params):
        """account 생성하는 함수

        account 함수 생성 후 id 반환

        Args:
            conn (class): DB 클래스
            params (dict): BODY에서 넘어온 user 회원가입 정보
        """
        sql = """
            INSERT INTO account (
                account_type_id
            )
            VALUES (
                %(account_type_id)s
            )
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.lastrowid
        
    def create_social_user_signup(self, conn, params):
        """social_user 생성하는 함수

        Args:
            conn (class): DB 클래스
            params (dict): BODY에서 넘어온 social user 회원가입 정보
        """
        sql = """
            INSERT INTO social_users (
                user_id,
                social_type_id,
                social_identification
            )
            VALUES (
                %(user_id)s,
                %(social_type_id)s,
                %(id)s
            )
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.lastrowid
    
    def create_user_signup(self, conn, params):
        """user 생성하는 함수

        Args:
            conn (class): DB 클래스
            params (dict): BODY에서 넘어온 user 회원가입 정보
        """
        print(params)
        if params['social'] == "google": 
            sql = """
                INSERT INTO users (
                    account_id,
                    user_type_id,
                    user_identification,
                    email,
                    receiving_event_is_agreed,
                    notifying_benefit_is_agreed   
                )
                VALUES (
                    %(account_id)s,
                    %(user_type_id)s,
                    %(id)s,
                    %(email)s,
                    %(receiving_event_is_agreed)s,
                    %(notifying_benefit_is_agreed)s
                )
            """
        elif params['user'] == "user":
            sql = """
                INSERT INTO users (
                    account_id,
                    user_type_id,
                    user_identification,
                    email,
                    password,
                    phone,
                    receiving_event_is_agreed,
                    notifying_benefit_is_agreed
                )
                VALUES (
                    %(account_id)s,
                    %(user_type_id)s,
                    %(id)s,
                    %(email)s,
                    %(password)s,
                    %(phone)s,
                    %(receiving_event_is_agreed)s,
                    %(notifying_benefit_is_agreed)s
                )
            """
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.lastrowid
    
    def create_user_history(self, conn, params):
        """user history 생성하는 함수

        Args:
            conn (class): DB 클래스
            params (dict): BODY에서 넘어온 user 회원가입 정보
        """
        if params['social'] == "google": 
            sql = """
                INSERT INTO users_history (
                    user_id,
                    receiving_event_is_agreed,
                    notifying_benefit_is_agreed
                ) VALUES (
                    %(user_id)s,
                    %(receiving_event_is_agreed)s,
                    %(notifying_benefit_is_agreed)s
                )
            """
        elif params['social'] == "user":
            sql = """
                INSERT INTO users_history (
                    user_id,
                    phone,
                    receiving_event_is_agreed,
                    notifying_benefit_is_agreed
                ) VALUES (
                    %(user_id)s,
                    %(phone)s,
                    %(receiving_event_is_agreed)s,
                    %(notifying_benefit_is_agreed)s
                )
            """
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.lastrowid
        
    def post_user_login(self, conn, params):
        """user 로그인

        Args:
            conn (class): DB 클래스
            params (dict): BODY에서 넘어온 user 정보
        """
        sql = """
            SELECT
                user_identification, password, is_deleted, account_id
            FROM
                users
            WHERE
                is_deleted = 0
                AND user_identification = %(id)s
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
    
    def post_social_login(self, conn, params):
        """social user 로그인 

        Args:
            conn (class): DB 클래스
            params ([type]): BODY에서 넘어온 social user 정보
        """
        sql = """
            SELECT
                user_identification, id_deleted, account_id
            FROM
                users
            WHERE
                is_deleted = 0,
                AND user_identifacation = %(id)s
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fechone()
     
    def get_social_user_identification(self, conn, params):
        """social users 중복 확인 하는 함수
        
        social 로그인을 하는데 가입된 아이디가 있는지 없는지 판단하는 함수

        Args:
            conn (class): DB 클래스
            params (dict): 구글 로그인 요청할 때 받아온 user 정보
        """
        sql = """
            SELECT
                social_identification
            FROM
                social_users
            WHERE
                social_identification = %(id)s
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
        pass