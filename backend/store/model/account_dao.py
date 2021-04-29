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
        
    def create_user_signup(self, conn, params):
        """user 생성하는 함수

        Args:
            conn (class): DB 클래스
            params (dict): BODY에서 넘어온 user 회원가입 정보
        """
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
    
    def cerate_user_history(self, conn, params):
        """user history 생성하는 함수

        Args:
            conn (class): DB 클래스
            params (dict): BODY에서 넘어온 user 회원가입 정보
        """
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
