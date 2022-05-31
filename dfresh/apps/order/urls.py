from django.urls import path
from .views import GetGoodsPayView, GetGoodsCartPayView, GetGoodsOrderPayView, GoodsPayResultView


app_name = 'order'
urlpatterns = [
    path('pay', GetGoodsPayView.as_view(), name='pay'),
    path('cartpay', GetGoodsCartPayView.as_view(), name='cartpay'),
    path('orderpay', GetGoodsOrderPayView.as_view(), name='orderpay'),
    path('rst', GoodsPayResultView.as_view(), name='rst'),
]