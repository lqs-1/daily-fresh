from django.views.generic import View
from django.shortcuts import redirect, render, reverse
from .models import GoodsType, IndexGoodsBanner, IndexTypeGoodsBanner, IndexPromotionBanner, GoodsSKU
from apps.order.models import OrderGoods
# from dfresh import settings
# from django.core.cache import cache
from django_redis import get_redis_connection
from redis import StrictRedis

from django.core.paginator import Paginator
'''
django使用redis的两种方式：
    第一种没有配置django_redis缓存：
        sr = StrictRedis(host=,port=,db=)
    第二种配置了django_redis缓存
        conn = get_redis_connection('default')

'''


class GetAndSetIndexView(View):
    """商品促销活动先不管"""
    def get(self, request):
        # 获取商品分类
        goods_type_list = GoodsType.objects.all().order_by("logo")[:6]
        # 获取banner轮播
        goods_index_goods_banner = IndexGoodsBanner.objects.all().order_by("index")
        # 获取活动
        active_goods_list = IndexPromotionBanner.objects.all()[:2]

        #  获取分类商品
        for goods_type in goods_type_list:
            image_banners = IndexTypeGoodsBanner.objects.filter(type=goods_type, display_type=1).order_by('index')[:4]
            text_banners = IndexTypeGoodsBanner.objects.filter(type=goods_type, display_type=1).order_by('index')[:4]

        #       动态添加属性
            goods_type.image_banners = image_banners
            goods_type.text_banners = text_banners

        context = {
            "goods_type_list": goods_type_list,
            "goods_index_goods_banner": goods_index_goods_banner,
            "active_goods_list": active_goods_list

        }

        return render(request, 'index.html', context)

class GetGoodsDetailView(View):
    def get(self, request, goods_id):
        goods = GoodsSKU.objects.get(id=goods_id)
        # 展示推荐商品
        show_goods_list = GoodsSKU.objects.filter(type=goods.type).order_by("-sales")[:2]
        # 同spu商品
        goods_list = GoodsSKU.objects.filter(goods=goods.goods)
        # print(goods_list)
        # 获取评论信息
        comments = OrderGoods.objects.filter(sku=goods.id)

        user = request.user

        if user.is_authenticated:
            # 放入历史浏览记录
            conn = get_redis_connection('default')
            key = f'history_{user.id}'
            # history = conn.lrange(key, 0, -1)
            # 移除列表中的goods_id
            conn.lrem(key, 0, goods_id)
            # 把goods_id插入到列表的左侧
            conn.lpush(key, goods_id)
            # 只保存用户最新浏览的5条信息
            # conn.ltrim(key, 0, 4)

        context = {
            'goods': goods,
            'show_goods_list': show_goods_list,
            'comments': comments,
            'goods_list': goods_list
        }
        return render(request, 'detail.html', context)

class GetGoodsListView(View):
    def get(self, request, goods_type_id, page):
        # print(goods_type_id)
        goods_type = GoodsType.objects.get(id=goods_type_id)
        goods_list = GoodsSKU.objects.filter(type=goods_type)
        goods_list_tj = goods_list[:2]

        paginator = Paginator(goods_list, 2)
        # 获取第n页
        # paginator.get_page(2)
        goods_list = paginator.get_page(page)

        # goods_list.has_previous()

        # 控制的显示页码
        num_pages = paginator.num_pages

        # 显示五个页码
        # 总页数小于5，显示全部
        if num_pages < 5:
            pages = range(1, num_pages+1)
        # 处于前三页
        elif page <= 3:
            pages = range(1, 6)
        # 处于后三页
        elif num_pages - page <= 2:
            pages = range(num_pages -4, num_pages+1)
        # 中间情况
        else:
            pages = range(page - 2, page + 3)

        context = {
            'goods_list': goods_list,
            'goods_list_tj': goods_list_tj,
            'goods_id': goods_type_id,
            'pages': pages,
            'goods_type': goods_type
        }
        # 以下是在页面渲染使用
        # # 是否有前一页
        # goods_list.has_previous()
        # # 是否有后一页
        # goods_list.has_next()
        # # 是否是当前页
        # goods_list.number()
        # # 便利页码
        # goods_list.paginator.page_range()
        # 下一页
        # goods_list.paginator.next_page_number
        # 上一页
        # goods_list.paginator.previous_page_number

        return render(request, 'list.html', context)


