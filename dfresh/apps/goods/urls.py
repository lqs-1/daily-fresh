from django.urls import path
from .views import GetAndSetIndexView,  GetGoodsDetailView, GetGoodsListView

app_name = 'goods'
urlpatterns = [
    path('', GetAndSetIndexView.as_view(), name='index'),
    path('detail/<int:goods_id>', GetGoodsDetailView.as_view(), name='detail'),
    path('list/<int:goods_type_id>/<int:page>', GetGoodsListView.as_view(), name='list')
]