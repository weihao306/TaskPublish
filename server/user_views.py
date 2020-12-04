from django.http import QueryDict
from django.shortcuts import render
from furl import furl  # 引入furl模块
from django.db import transaction  # 引入数据库事务模块
from django.shortcuts import redirect  # 引入重定向方法
from django.views.decorators.csrf import csrf_exempt  # 引入防跨站请求伪造装饰器
from django.conf import settings  # 项目配置模块
from io import BytesIO  # 流传输模块
from utils.response import __response_data, json_response  # 引入响应对象
from server.models import Profile  # 引入Profile数据模型
from django.core import serializers  # 引入序列化方法


# Create your views here.

@csrf_exempt  # POST表单防止跨站请求伪造
@transaction.atomic  # 数据库操作失败回滚
def register(request):
    """
    用户注册模块
    """
    account = request.POST.get('account', '')  # 获取用户名
    password = request.POST.get('password', '')  # 获取密码
    city = request.POST.get('city', '')  # 获取城市
    introduction = request.POST.get('introduction', '')  # 获取用户简介
    cert_type = request.POST.get('cert_type', '')  # 证件类型
    cert_number = request.POST.get('cert_number', '')  # 证件号
    phone = request.POST.get('telephone', 0)  # 电话号码
    name = request.POST.get('name', '')  # 姓名

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
            'uid': Profile.objects.get(account=account).uid
        })
    else:
        return json_response(300003, 'User Has Existed', {})


@csrf_exempt
@transaction.atomic
# @require_http_methods(["POST"])
def login(request):
    """
    用户登录模块
    """
    
    account = request.POST.get('account', '')
    password = request.POST.get('password', '')
    # account = request.POST['account']
    # password = request.POST['password']

    p = Profile.objects.filter(account__exact='admin')
    if p.__len__() is 0:
        return json_response(300001, 'User Not Found', {})
    else:
        if p.password != password:
            return json_response(300002, 'Password Error', {})
        else:
            return json_response((200, 'OK', {
                'uid': p.uid
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
    uid = request.GET.get('uid', '')  # 获取用户uid
    try:
        p = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:
        return json_response(300001, 'User Not Found', {})
    else:
        return json_response(200, 'OK', serializers.serialize('json', p))


@transaction.atomic
def update_info(request):
    """
    修改用户信息
    """
    put = QueryDict(request.body)
    try:
        uid = put.get('uuid', '')
        p = Profile.objects.get(uid=uid)
    except Profile.DoesNotExist:
        return json_response(300001, 'User Not Found', {})
    else:
        p.password = put.get('password', '')
        p.phone = put.get('telephone', '')
        p.introduction = put.get('introduction', '')
        p.user_name = put.get('nickname', '')
        p.save()
        return json_response(200, 'OK', {})
