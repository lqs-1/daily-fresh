from django.urls import path
from .views import GetGoodsCartView, AddGoodsCartView, DeleteGoodsCartView

app_name = 'cart'
urlpatterns = [
    path('cart', GetGoodsCartView.as_view(), name='cart'),
    path('add', AddGoodsCartView.as_view(), name='add'),
    path('delete', DeleteGoodsCartView.as_view(), name='delete'),
]