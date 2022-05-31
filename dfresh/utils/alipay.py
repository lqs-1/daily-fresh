from alipay import AliPay
# pip install python-alipay-sdk
from dfresh import settings

app_private_key_str = settings.APP_PRIVATE_KEY_STR
alipay_public_key_str = settings.ALIPAY_PUBLIC_KEY_STR


def gen_alipay_client():
    alipay_client = AliPay(
        appid="2021000118649112",  # 支付宝开放平台的appid
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_str,  # 应用私钥
        alipay_public_key_string=alipay_public_key_str,  # 支付宝公钥
        sign_type='RSA2',  # RSA或者RSA2
        debug=True,  # True为沙箱
    )
    return alipay_client




