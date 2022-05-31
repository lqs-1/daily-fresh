from utils import alipay


def pay():
    rst = alipay.gen_alipay_client().api_alipay_trade_page_pay(
        out_trade_no=1,  # 订单编号
        total_amount="3",  # 总金额
        subject='fsdf',  # 订单主题
        return_url='https://www.baidu.com',  # 支付成功跳转页面
        notify_url=None,  # 回调地址
    )
    return "https://openapi.alipaydev.com/gateway.do?" + rst

if __name__ == '__main__':
    # 电脑网站支付
    print(pay())
