import json
import logging
import sys

from django.core import serializers  # 引入序列化方法
from django.db import transaction  # 引入数据库事务模块
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt  # 引入防跨站请求伪造装饰器

from server.models import Profile  # 引入Profile数据模型
from utils.response import json_response  # 引入响应对象


# Create your views here.

@csrf_exempt  # POST表单防止跨站请求伪造
@transaction.atomic  # 数据库操作失败回滚
def register(request):
    """
    用户注册模块
    """
    body = json.loads(request.body)            # 获取请求内容
    account = body.get('account', '')       # 获取用户名
    password = body.get('password', '')     # 获取密码
    city = body.get('city', '')             # 获取城市
    introduction = body.get('introduction', '')     # 获取用户简介
    cert_type = body.get('cert_type', '')           # 证件类型
    cert_number = body.get('cert_number', '')       # 证件号
    phone = body.get('telephone', 0)        # 电话号码
    name = body.get('name', '')             # 姓名

    try:
        p = Profile.objects.get(account=account)
    except Profile.DoesNotExist:  # 用户信息不存在
        Profile.objects.create(  # 创建新用户信息并写入数据库
            account=account,
            password=password,
            city=city,
            introduction=introduction,
            cert_type=cert_type,
            cert_number=cert_number,
            phone=phone,
            user_name=name,
            user_type=1,
            user_level=0,
        )
        return json_response(200, 'OK', {  # 返回用户uid
            'uid': Profile.objects.get(account=account).value().get('uid')
        })
    else:
        return json_response(300003, 'User Has Existed', {})


@csrf_exempt
@transaction.atomic
def login(request):
    """
    用户登录模块
    """
    body = json.loads(request.body)
    account = body.get('account', '')
    password = body.get('password', '')

    try:
        p = Profile.objects.values().get(account=account)
    except Profile.DoesNotExist:
        return json_response(300001, 'User Not Found', {})
    else:
        if p.get('password') != password:
            return json_response(300002, 'Password Error', {})
        else:
            return json_response((200, 'OK', {
                'uid': p.get('uid')
            }))


def info(request):
    """
    用户信息管理
    """
    if request.method == 'GET':
        get_info(request)
    elif request.method == 'PUT':
        update_info(request)


@csrf_exempt
@transaction.atomic
def get_info(request):
    """
    查询用户信息
    """
    body = json.loads(request.body)
    uid = body.get('uid', '')  # 获取用户uid
    try:
        p = Profile.objects.get(uid=uid).value()
    except Profile.DoesNotExist:
        return json_response(300001, 'User Not Found', {})
    else:
        return json_response(200, 'OK', serializers.serialize('json', p))


@transaction.atomic
def update_info(request):
    """
    修改用户信息
    """
    body = json.loads(request.body)
    try:
        uid = body.get('uuid', '')
        p = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:
        return json_response(300001, 'User Not Found', {})
    else:
        p.password = body.get('password', '')
        p.phone = body.get('telephone', '')
        p.introduction = body.get('introduction', '')
        p.user_name = body.get('nickname', '')
        p.save()
        return json_response(200, 'OK', {})
