from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from utils.loginCheck import LoginRequiredMixin
from utils import alipay, statusCode
from .models import OrderGoods, OrderInfo
from apps.goods.models import GoodsSKU
from apps.user.models import Address
from django.db import transaction
import logging
from dfresh import settings
import uuid
from apps.cart.models import GoodsCart

logger = logging.getLogger('django')

# # 电脑网站支付
# alipay.gen_alipay_client().api_alipay_trade_page_pay(
#     out_trade_no=1,  # 订单编号
#     total_amount=3,  # 总金额
#     subject='fsdf',  # 订单主题
#     return_url='http',  # 支付成功跳转页面
#     notify_url=None,  # 回调地址
# )


class GetGoodsPayView(LoginRequiredMixin, View):
    """直接购买"""
    def get(self, request):
        goods_name = request.GET.get('goods_name')
        goods_count = request.GET.get('goods_count')
        goods_totail = request.GET.get('goods_totail')
        goods = GoodsSKU.objects.get(name=goods_name)

        if not all([goods_totail, goods_name, goods_count]):
            return redirect('goods:detail', goods.id)

        address_list = Address.objects.filter(user=request.user)
        context = {
            'errno': statusCode.OK,
            'errmsg': 'ok',
            'goods': goods,
            'goods_count': goods_count,
            'goods_totail': goods_totail,
            'address_list': address_list
        }

        return render(request, 'place_order.html', context)

    def post(self, request):
        address_id = request.POST.get('address_id')
        paystyle_id = request.POST.get('paystyle_id')
        totail_count = request.POST.get('totail_count')
        totail_price = request.POST.get('totail_price')
        goods_id = request.POST.get('goods_id')

        try:
            with transaction.atomic():
                goods = GoodsSKU.objects.get(id=goods_id)
                order_id = uuid.uuid1().hex
                order_info = OrderInfo.objects.create(
                    order_id=order_id,
                    user=request.user,
                    addr=Address.objects.get(id=address_id),
                    pay_method=paystyle_id,
                    total_price=totail_price,
                    total_count=totail_count,
                    transit_price=0,
                    trade_no=order_id,
                )

                order_info.save()
                order_goods = OrderGoods.objects.create(
                    order=order_info,
                    sku=goods,
                    count=totail_count,
                    price=totail_price,
                )
                order_goods.save()
        except Exception as e:
            logger.error(f'{e}, {request.user.username}的订单保存失败')
            url = 'http://127.0.0.1:8000/goods/detail/' + goods.id
            return JsonResponse({'errno': statusCode.DB_ERROR, 'errmsg': '订单保存失败', 'url': url})

        # 沙箱账号：   rfwqto6283@sandbox.com

        try:
            # 电脑网站支付
            pay_string = alipay.gen_alipay_client().api_alipay_trade_page_pay(
                out_trade_no=order_info.order_id,  # 订单编号
                total_amount=totail_price,  # 总金额
                subject='天天生鲜' + goods.name,  # 订单主题
                return_url='http://127.0.0.1:8000/order/rst',  # 支付成功跳转页面,后期修改到自己的接口进行验证然后改状态
                notify_url=None,  # 回调地址
            )
        except Exception as e:
            logger(f'{e}, {request.user.username}支付失败')
            url = 'http://127.0.0.1:8000/user/order'
            return JsonResponse({'errno': statusCode.NET_WORD_CONNECTION_PAY_ERROR, 'errmsg': '订单保存失败', 'url': url})
        pay_url = settings.ALIPAY_BASE_URL + pay_string
        return JsonResponse({'errno': statusCode.OK, 'errmsg': '支付成功', 'pay_url': pay_url})


# 上面是垃圾方法，直接购买的，下面紧挨着的两个视图是结算购物车
class GetGoodsCartPayView(LoginRequiredMixin, View):
    def get(self, request):
        goods_id_list = request.GET.getlist('goods_id')

        if goods_id_list is None:
            return redirect("cart:cart")

        cart_goods_list = list()
        goods_count_totail = 0
        goods_price_totail = 0
        for goods_id in goods_id_list:
            cart_goods = GoodsCart.objects.get(goods_id=goods_id, user=request.user)
            cart_goods.totail = cart_goods.price * cart_goods.count
            goods_count_totail += cart_goods.count
            goods_price_totail += cart_goods.totail
            cart_goods_list.append(cart_goods)

        address_list = Address.objects.filter(user=request.user)

        context = {
            'errno': statusCode.OK,
            'errmsg': 'ok',
            'cart_goods_list': cart_goods_list,
            'address_list': address_list,
            'goods_count_totail': goods_count_totail,
            'goods_price_totail': goods_price_totail
        }

        return render(request, 'place_cart_order.html', context)

    def post(self, request):
        address_id = request.POST.get('address_id')
        cart_id_list = request.POST.getlist('cart_id')
        pay_style = request.POST.get('pay_style')

        if not all([address_id, cart_id_list, pay_style]):
            return redirect("cart:cart")
            logger.error("数据不完整")

        or_id = uuid.uuid1().hex
        try:
            with transaction.atomic():
                order_info = OrderInfo.objects.create(
                    order_id=or_id,
                    user=request.user,
                    addr=Address.objects.get(id=address_id),
                    pay_method=pay_style,
                    transit_price=0,
                    trade_no=or_id,
                    total_price=2,
                    total_count=2,
                )
                order_info.save()

                order_info_totail_price = 0
                order_info_totail_count = 0

                for cart_id in cart_id_list:
                    cart_id = int(cart_id)
                    cart_goods = GoodsCart.objects.get(id=cart_id)
                    totail_price = cart_goods.count * cart_goods.price
                    totail_count = cart_goods.count
                    order_goods = OrderGoods.objects.create(
                        order=order_info,
                        sku=cart_goods.goods,
                        count=totail_count,
                        price=totail_price,
                    )

                    cart_goods.delete()

                    order_goods.save()
                    order_info_totail_price += totail_price
                    order_info_totail_count += totail_count

                order_info.total_count = order_info_totail_count
                order_info.total_price = order_info_totail_price

                order_info.save()

        except Exception as e:
            logger.error(f'{e}, {address_id}地址的购物车结算失败')
            return redirect("cart:cart")

        try:

            # 电脑网站支付
            pay_string = alipay.gen_alipay_client().api_alipay_trade_page_pay(
                out_trade_no=or_id,  # 订单编号
                total_amount=str(order_info_totail_price),  # 总金额
                subject='天天生鲜' + order_info.order_id,  # 订单主题
                return_url='http://127.0.0.1:8000/order/rst',  # 支付成功跳转页面,后期修改到自己的接口进行验证然后改状态
                notify_url=None,  # 回调地址
            )

        except Exception as e:
            logger.error(f'{e}, {request.user.username}支付失败')
            return redirect("cart:cart")

        pay_url = settings.ALIPAY_BASE_URL + pay_string

        return redirect(pay_url)


class GetGoodsOrderPayView(View):
    '''订单页面支付'''
    def post(self, request):
        order_id = request.POST.get('order_id')

        order_info = OrderInfo.objects.get(order_id=order_id)

        try:

            # 电脑网站支付
            pay_string = alipay.gen_alipay_client().api_alipay_trade_page_pay(
                out_trade_no=order_info.order_id,  # 订单编号
                total_amount=str(order_info.total_price),  # 总金额
                subject='天天生鲜' + order_info.order_id,  # 订单主题
                return_url='http://127.0.0.1:8000/order/rst',  # 支付成功跳转页面,后期修改到自己的接口进行验证然后改状态
                notify_url=None,  # 回调地址
            )

        except Exception as e:
            logger.error(f'{e}, {request.user.username}支付失败')
            return redirect("cart:cart")
        pay_url = settings.ALIPAY_BASE_URL + pay_string
        return redirect(pay_url)


# 订单支付完成以后判断支付状态，修改订单表状态，修改商品数量（库存）
class GoodsPayResultView(View):
    def get(self, request):
        '''改状态， 修改商品数量'''
        pass










