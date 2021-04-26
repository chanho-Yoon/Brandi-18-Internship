from .product_view import (
                            ProducListtView,
                            ProductDetailView,

)

from .order_view import (
                            OrderListView,

)

from .account_view import (
                            SignUpView,
                            SignInView,
                            SocialSignInView,
                            MyPageView
)           

from utils.error_handler import error_handle


def create_endpoints(app, services):
    product_service = services.product_service
    order_service = services.order_service
    account_service = services.account_service


    # product
    app.add_url_rule("/products",
                    view_func=ProductListView.as_view('product_view', product_service), 
                    methods=['GET'])

    app.add_url_rule("/products/<product_code>", 
                    view_func=ProductDetailView.as_view('product_detail_view', product_service), 
                    methods=['GET', 'POST', 'PATCH'])

    # order
    app.add_url_rule("/order",
                    view_func=OrderListView.as_view('order_view', order_service),
                    methods=['GET', 'POST', 'PATCH'])
    
    # account
    app.add_url_rule("/signup",
                    view_func=SignUpView.as_view('signup_view', account_service),
                    methods=['POST'])
    
    app.add_url_rule("/signin",
                    view_func=SignInView.as_view('signin_view', account_service),
                    methods=['POST'])

    app.add_url_rule("/signin/social",
                    view_func=SocialSignInView.as_view('social_signin_view', account_service),
                    methods=['POST'])

    app.add_url_rule("/mypage",
                    view_func=MyPageView.as_view('mypage_view', account_service),
                    methods=['GET', 'POST', 'PATCH'])

