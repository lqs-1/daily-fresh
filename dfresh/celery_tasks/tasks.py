from celery import Celery
import os

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dfresh.settings')
django.setup()

from django.core.mail import send_mail
from dfresh import settings


app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/0')


@app.task
def send_mail_tasks(username, email, token):
    object = f'天天生鲜用户{username}注册激活邮件'  # 主题
    message = ''  # 必填， 没有也要填，不能写html代码，因为不能转意
    from_email = settings.EMAIL_FROM   # 谁发
    recipient_list = [email]   # 发给谁
    html_message = f'<h3>您好,{username}:</h3><br><h5>请点击链接完成注册激活:<br><a href="http://127.0.0.1:8000/user/active/{token}">http://127.0.0.1:8000/user/active/{token}</a><br>激活后才可以登录账号，请在5分钟之内激活否则链接失效</h5>'  # 写html代码， 可以转意
    send_mail(object, message, from_email, recipient_list, html_message=html_message)