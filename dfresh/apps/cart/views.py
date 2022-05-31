from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from .models import GoodsCart
from utils.loginCheck import LoginRequiredMixin
from ..goods.models import GoodsSKU
from utils import statusCode
import logging
from django.db import transaction
# from django_redis import get_redis_connection

logger = logging.getLogger('django')


'''
后期优化第三方缓存技术
'''


class GetGoodsCartView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_cart_list = GoodsCart.objects.filter(user=user.id)

        for user_cart in user_cart_list:
            price = user_cart.price
            count = user_cart.count

            totail = price * count
            user_cart.totail = totail

        context = {
            'user_cart_list': user_cart_list,
        }
        return render(request, 'cart.html', context)


class AddGoodsCartView(LoginRequiredMixin, View):
    def post(self, request):
        goods_id = request.POST.get('goods_id')
        goods_name = request.POST.get('goods_name')
        goods_price = request.POST.get('goods_price')
        goods_unit = request.POST.get('goods_unit')
        goods_count = request.POST.get('goods_count')

        if not all([goods_price, goods_count, goods_unit, goods_name, goods_id]):
            return JsonResponse({'errno': statusCode.INCOMPLETE_DATA, 'errmsg': '数据不完整'})

        # 转换价格格式
        goods_price = goods_price[1:]
        # 数量
        goods_count = goods_count.replace("数 量：", "")
        # 单位
        goods_unit = goods_unit.replace("单  位：", "")

        # 判断是否已经有购物车信息
        try:
            with transaction.atomic():
                cart = GoodsCart.objects.get(name=goods_name)
        except Exception as e:
                cart = None

        # 保存购物车
        user = request.user
        try:
            with transaction.atomic():
                goods = GoodsSKU.objects.get(id=goods_id)
                if cart is not None:
                    try:
                        with transaction.atomic():
                            goods_count = int(goods_count)
                            cart.count += goods_count
                            cart.save()
                        return JsonResponse({'errno': statusCode.OK, 'errmsg': '添加成功'})
                    except Exception as e:
                        logger.error(f'{e}, 保存到数据库失败')
                        return JsonResponse({'errno': statusCode.DB_ERROR, 'errmsg': '数据库链接失败'})
                try:
                    with transaction.atomic():
                        cart = GoodsCart.objects.create(name=goods_name, price=goods_price, count=goods_count,
                                                        unite=goods_unit, user=user, goods=goods)
                        cart.save()
                except Exception as e:
                    logger.error(f'{e}, 商品添加购物车失败')
                    return JsonResponse({'errno': statusCode.DB_ERROR, 'errmsg': '数据库链接失败'})

                return JsonResponse({'errno': statusCode.OK, 'errmsg': '添加成功'})
        except Exception as e:
            logger.error(f'{e}, 没有此用户')
            return JsonResponse({'errno': statusCode.DB_ERROR, 'errmsg': '数据库链接失败'})


class DeleteGoodsCartView(LoginRequiredMixin, View):
    def post(self, request):
        goods_name = request.POST.get('goods_name')
        # print(goods_name)
        try:
            with transaction.atomic():
                GoodsCart.objects.get(name=goods_name).delete()
        except Exception as e:
            logger.error(f'{e}, 删除购物车商品失败，数据库链接失败')
            return JsonResponse({'errno': statusCode.DB_ERROR, 'errmsg': '数据库链接错误'})
        return JsonResponse({'errno': statusCode.OK, 'errmsg': '删除成功'})

