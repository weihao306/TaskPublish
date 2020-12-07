import json
import logging
import sys

from django.core import serializers  # 引入序列化方法
from django.db import transaction  # 引入数据库事务模块
from django.http import QueryDict
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt  # 引入防跨站请求伪造装饰器

from server.models import Profile  # 引入Profile数据模型
from utils.response import json_response  # 引入响应对象
# from django.http import JsonResponse

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
    cert_type = body.get('cert_type', 0)           # 证件类型
    cert_number = body.get('cert_number', '')       # 证件号
    phone = body.get('telephone', 0)        # 电话号码
    name = body.get('nick_name', '')             # 姓名

    try:
        p = Profile.objects.get(account=account)
    except Profile.DoesNotExist:  # 用户信息不存在
        with transaction.atomic():
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
            'uid': Profile.objects.values().get(account=account).get('uid')
        })
    else:
        return json_response(300003, 'User Has Existed', {'error': True})


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
        return HttpResponseBadRequest("没有该用户")
    else:
        if p.get('password') != password:
            return HttpResponseBadRequest("密码错误")
        else:
            return json_response(200, "OK", {
                'uid': p.get('uid'),
                'nick_name': p.get('user_name'),
                'account': p.get('account'),
                'introduction': p.get('introduction'),
                'telephone': p.get('phone'),
                'cert_type': p.get('cert_type'),
                'cert_number': p.get('cert_number')
            })


@csrf_exempt
def info(request):
    """
    用户信息管理
    """
    if request.method == 'GET':
        return get_info(request)
    elif request.method == 'PUT':
        return update_info(request)


@transaction.atomic
def get_info(request):
    """
    查询用户信息
    """
    # body = json.loads(request.body)
    body = request.GET
    uid = body.get('uid', '')  # 获取用户uid
    try:
        p = Profile.objects.values().get(uid=uid)
    except Profile.DoesNotExist:
        return json_response(300001, 'User Not Found', {})
    else:
        return json_response(200, "OK", {
            'uid': p.get('uid'),
            'nick_name': p.get('user_name'),
            'account': p.get('account'),
            'introduction': p.get('introduction'),
            'telephone': p.get('phone'),
            'cert_type': p.get('cert_type'),
            'cert_number': p.get('cert_number')
        })


@transaction.atomic
def update_info(request):
    """
    修改用户信息
    """
    body = json.loads(request.body)
    # body = request.GET
    try:
        uid = body.get('uid', '')
        p = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:
        return json_response(300001, 'User Not Found', {})
    else:

        p.password = body.get('password', p.password) if body.get(
            'password', '') != '' else p.password

        p.phone = body.get('telephone', p.phone)
        p.introduction = body.get('introduction', p.introduction)
        p.user_name = body.get('nick_name', p.user_name) if body.get(
            'nick_name', '') != '' else p.user_name
        p.save()
        return json_response(200, 'OK', {})
