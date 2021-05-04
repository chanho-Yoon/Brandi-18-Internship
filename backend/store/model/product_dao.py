
class ProductDao:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

class ProductDao:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

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

