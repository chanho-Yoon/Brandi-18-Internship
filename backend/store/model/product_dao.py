from utils.custom_exception import DataNotExists

class ProductDao:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass
    
    # 데이터베이스에 상품이 존재하는지 확인
    def check_product_exists(self, conn, params):
        sql = """
            SELECT
                COUNT(0) as count
            FROM
                products as p
            WHERE
                p.id = %(product_id)s
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    # 상품 상세 정보 가져오기
    def get_product_detail(self, conn, params):
        # 상품 상세 정보 가져오기
        product_detail_sql = """
            SELECT
                s.korean_brand_name as seller_korean_name,
                s.id as seller_id,
                p.title as title,
                p.price as price,
                IF(p.discount_start_date <= now() AND p.discount_end_date >= now(), TRUNCATE(p.discount_rate, 2), 0) as discount_rate,
                p.content as detail_description,
                p.id as product_id
            FROM
                products as p
            INNER JOIN
                sellers as s
                ON s.id = p.seller_id
            WHERE
                p.id = %(product_id)s
        """
        # 상품 이미지 가져오기
        image_sql = """
            SELECT
                pi.image_url,
                pi.is_represent
            FROM
                product_images as pi
            WHERE
                pi.product_id = %(product_id)s
            AND
                pi.is_deleted = 0
        """
        # 상품 옵션 정보 가져오기
        option_sql = """
            SELECT 
                o.id as option_id,
                o.size_id as size_id,
                o.color_id as color_id,
                s.name as size_name,
                c.name as color_name,
                o.price as price,
                o.stock as stock
            FROM
                options as o
            INNER JOIN
                color as c
                ON c.id = o.color_id
            INNER JOIN
                size as s
                ON s.id = o.size_id
            WHERE
                o.product_id = %(product_id)s
            AND
                o.is_deleted = 0
        """
        # 셀러 다른 상품 가져오기
        other_product_sql = """
            SELECT
                p.id as product_id,
                pi.image_url as image_url,
                p.title as title,
                p.price,
                IF(p.discount_start_date <= now() AND p.discount_end_date >= now(), TRUNCATE(p.discount_rate, 2), 0) as discount_rate,
                discount_start_date,
                discount_end_date
            FROM
                products as p
            INNER JOIN
                product_images as pi
                ON pi.product_id = p.id
                AND pi.is_represent = 1
                AND pi.is_deleted = 0
            WHERE
                p.seller_id = %(seller_id)s
            ORDER BY
                p.created_at DESC
            LIMIT
                5
        """

        with conn.cursor() as cursor:
            cursor.execute(product_detail_sql, params)
            product_detail = cursor.fetchone()
            
            # 데이터베이스에 상품 존재하는지 확인
            if not product_detail:
                raise DataNotExists('상품이 존재하지 않습니다.', 'product does not exist')
            
            cursor.execute(image_sql, params)
            product_image = cursor.fetchall()
            cursor.execute(option_sql, params)
            product_option = cursor.fetchall()
            cursor.execute(other_product_sql, product_detail)
            other_product = cursor.fetchall()

            return product_detail, product_image, product_option, other_product

    # 상품 질문, 응답 가져오기
    def get_product_question_answer(self, conn, request_data):
        # 질문 정보 가져오기
        question_sql = """
            SELECT
                q.id as question_id,
                q.created_at as question_upload_date,
                qt.id as question_type_id,
                qt.name as question_type_name,
                q.answer_status as question_answer_status,
                q.content as question_content,
                q.user_id as question_user_id,
                u.user_identification as question_user_identification,
                q.secret_status as question_secret_status,
                u.account_id as account_id
            FROM
                questions as q
            INNER JOIN
                question_type as qt
                ON qt.id = q.question_type_id
            INNER JOIN
                users as u
                ON u.id = q.user_id
            WHERE
                q.product_id = %(product_id)s
            AND
                q.is_deleted = 0
            ORDER BY
                q.created_at DESC
            LIMIT
                %(limit)s
            OFFSET
                %(offset)s
        """
        # 답변 정보 가져오기
        answer_sql = """
            SELECT
                a.id as answer_id,
                a.created_at as answer_upload_date,
                ac.id as account_id,
                a.content as answer_content,
                a.question_id as answer_question_id,
                CONCAT(IFNULL(s.korean_brand_name,''), IF(m.email IS NULL,'', '브랜디마스터')) as name
            FROM
                answers as a
            INNER JOIN
                questions as q
                ON q.id = a.question_id
            INNER JOIN
                account as ac
                ON ac.id = a.account_id
            LEFT JOIN
                sellers as s
                ON s.account_id = a.account_id
            LEFT JOIN
                master as m
                ON m.account_id = a.account_id
            WHERE
                a.question_id IN %(question_ids)s
            AND
                a.is_deleted = 0
        """
        
        with conn.cursor() as cursor:
            cursor.execute(question_sql, request_data)
            question_result = cursor.fetchall()
            
            # 해당 page에 질문이 없다면 return
            if not question_result:
                answer_result = []
                return question_result, answer_result
            
            # 답변 정보를 찾기 위해 질문 아이디 tuple 형태로 변환
            question_ids = tuple(map(lambda d:d.get('question_id'), question_result))
            question_ids = {'question_ids' : question_ids}

            cursor.execute(answer_sql, question_ids)
            answer_result = cursor.fetchall()
            return question_result, answer_result

    # 질문 총 개수 가져오기
    def get_total_count_question(self, conn, request_data):
        count_question_sql = """
            SELECT
                COUNT(0) as total_count
            FROM
                questions as q
            WHERE
                q.product_id = %(product_id)s
            AND
                q.is_deleted = 0
        """
        with conn.cursor() as cursor:
            cursor.execute(count_question_sql, request_data)
            return cursor.fetchone()

    def get_product_list(self, conn, dc_params):
        # 대표이미지 상호 상품명 할인율  (할인)가격  원가격 판매량 할인시작,종료
        sql = """ 
                SELECT 
                    pi.image_url AS product_img,
                    se.english_brand_name AS store_name, 
                    pr.title AS product_name,     
                    pr.price AS price_origin,	
                    pr.id AS product_id,
                    pr.discount_start_date AS discount_start,
                    pr.discount_end_date AS discount_end,
                    pr.discount_rate AS discounted_rate,
                    IF(pr.discount_start_date <= now() AND pr.discount_end_date >= now(), 
                            (pr.price*(1- pr.discount_rate)), null) AS price_discounted,
                    IFNULL((SELECT SUM(quantity)
                    FROM orders_detail AS od 
                        WHERE pr.id = od.product_id), null) AS product_sold
                                
                FROM products AS pr

                INNER JOIN sellers AS se
                    ON se.id = pr.seller_id
                    
                INNER JOIN product_images AS pi
                    ON pr.id = pi.product_id
                    AND pi.is_represent=1
                    
                WHERE pr.is_displayed=1 

                ORDER BY pr.created_at DESC

                LIMIT %(limit)s 

                OFFSET %(offset)s;
            """

        with conn.cursor() as cursor:
            cursor.execute(sql, dc_params)
            result = cursor.fetchall()
        
        return result
