from django.db import models
from db.base_model import BaseModel
# Create your models here.
class GoodsCart(BaseModel, models.Model):
    name = models.CharField(max_length=20, verbose_name='商品名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    unite = models.CharField(max_length=20, verbose_name='商品单位')
    count = models.IntegerField(verbose_name='商品数量')
    user = models.ForeignKey('user.User', verbose_name='用户', on_delete=models.CASCADE)
    goods = models.ForeignKey('goods.GoodsSKU', verbose_name='商品', on_delete=models.CASCADE, default=None)

    class Meta:
        db_table = 'df_user_cart'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
