from django.contrib import admin
from .models import Goods, GoodsSKU, GoodsImage, GoodsType, IndexTypeGoodsBanner, IndexGoodsBanner, IndexPromotionBanner


admin.site.register(Goods)
admin.site.register(GoodsSKU)
admin.site.register(GoodsImage)
admin.site.register(GoodsType)
admin.site.register(IndexTypeGoodsBanner)
admin.site.register(IndexGoodsBanner)
admin.site.register(IndexPromotionBanner)

# Register your models here.
