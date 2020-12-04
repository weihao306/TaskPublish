from django.http import QueryDict  # 引入QueryDict模块
from django.shortcuts import render
from furl import furl  # 引入furl模块
from django.db import transaction  # 引入数据库事务模块
from django.shortcuts import redirect  # 引入重定向方法
from django.views.decorators.csrf import csrf_exempt  # 引入防跨站请求伪造装饰器
from django.conf import settings  # 项目配置模块
from io import BytesIO  # 流传输模块
from utils.response import json_response  # 引入响应对象
from server.models import Task, Profile, Request, Success, Income  # 引入数据模型
from django.core import serializers  # 引入序列化方法
import json
from utils.timeformat import format_date  # 格式化时间字符串


def manage_request(request):
    """
    令主请求管理模块
    """
    body = QueryDict(request.body)
    option = body.get('option', '')
    if option == '00':
        master_query(request)
    elif option == '01':
        master_update(request)
    elif option == '10':
        slave_create(request)
    elif option == '11':
        slave_modify(request)
    elif option == '12':
        slave_query(request)


@csrf_exempt  # POST表单防止跨站请求伪造
@transaction.atomic  # 数据库操作失败回滚
def master_query(request):
    """
    查询请求信息
    """
    task = request.GET.get('order_id', '')
    try:
        req = Request.objects.filter(task__exact=task)
    except Request.DoesNotExist:
        return json_response(400001, 'Request Not Found', {})
    else:
        return json_response(200, 'OK', serializers.serialize('json', req))


@csrf_exempt  # POST表单防止跨站请求伪造
@transaction.atomic  # 数据库操作失败回滚
def master_update(request):
    """
    更新召集令请求状态
    """
    body = QueryDict(request.body)
    rid = body.get('request_id', '')
    time = body.get('time', '')
    status = body.get('state')

    if status == 'accepted':
        status = 1
        task_success(rid, time)
    elif status == 'denied':
        status = 2

    try:
        req = Request.objects.filter(uid__exact=rid)
        req.request_status = status
        req.save()
    except Exception as e:
        return json_response(400002, 'Accept Request Error', {'error': str(e)})
    else:
        data = Request.objects.filter(uid__exact=rid)
        return json_response(200, 'OK', serializers.serialize('json', data))


@transaction.atomic  # 数据库操作失败回滚
def task_success(rid, time):
    """
    召集成功写入数据库
    """
    req = Request.objects.filter(uid__exact=rid)
    master = req.task.master
    slave = req.requester
    master_cost = 3
    slave_cost = 1
    complete_date = req.updated_at
    try:
        Success.objects.create(
            request=req,
            master=master,
            slave=slave,
            master_cost=master_cost,
            slave_cost=slave_cost,
            complete_date=time,
        )
    except Exception as e:
        pass
    finally:
        add_income(rid, time)


@transaction.atomic  # 数据库操作失败回滚
def add_income(rid, time):
    """
    收入统计
    """
    date = format_date(time)        # 达成日期
    req = Request.objects.filter(uid__exact=rid)    # 查询请求
    ttype = req.task.task_type       # 召集令类型
    city = req.task.master.city     # 城市
    cost = 4        # 完成一次召集令请求的收入
    try:
        inc = Income.objects.filter(task_type=ttype, date=date, city=city)
    except Income.DoesNotExist:
        Income.objects.create(
            task_type=ttype,
            date=date,
            city=city,
            task_number=1,
            cost=cost,
        )
    else:
        inc.task_number += 1
        inc.cost += cost


@csrf_exempt  # POST表单防止跨站请求伪造
@transaction.atomic  # 数据库操作失败回滚
def slave_create(request):
    """
    接令者申请召集令
    """
    task = request.POST.get('order_id', '')
    req = request.POST.get('slave_id', '')
    desc = request.POST.get('request_msg', '')

    try:
        Request.objects.create(
            task=task,
            requester=req,
            description=desc,
        )
    except Exception as e:
        return json_response(400003, 'Create Request Error', {'error': str(e)})
    else:
        data = Request.objects.filter(task__exact=task, requester__exact=req)
        return json_response(200, 'OK', serializers.serialize('json', data))


@transaction.atomic
def slave_modify(request):
    """
    接令者修改申请信息
    """
    body = QueryDict(request.body)
    req = body.get('request_id', '')
    msg = body.get('request_msg', '')

    try:
        Request.objects.get(uid=req).update(description=msg)
    except Exception as e:
        return json_response(400004, 'Modify Request Error', {'error': str(e)})
    else:
        return json_response(200, 'OK', {})


@transaction.atomic
def slave_query(request):
    """
    接令人查询已经接受的召集令请求
    """
    slave = request.GET.get('slave_uuid', '')
    try:
        task = Request.objects.filter(requester__exact=slave, request_status__exact=1)
    except Exception as e:
        return json_response(400005, 'Slave Query Error', {'error': str(e)})
    else:
        return json_response(200, 'OK', serializers.serialize('json', task))


@transaction.atomic
def slave_delete(request):
    """
    接令人删除为同意的召集令请求
    """
    body = QueryDict(request.body)
    req = body.get('request_id', '')
    try:
        Request.objects.filter(uid__exact=req, request_status__exact=0).delete()
    except Request.DoesNotExist:
        return json_response(400006, 'Delete Request Not Exist', {})
    else:
        return json_response(200, 'OK', {})
