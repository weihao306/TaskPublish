from datetime import date, datetime
from os import name
from django.db.models.fields import DateField
from django.http import QueryDict
# 引入QueryDict模块
from django.http.response import HttpResponseBadRequest, HttpResponseServerError
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
import MySQLdb


@csrf_exempt  # POST表单防止跨站请求伪造
def manage_request(request):
    """
    令主请求管理模块
    """
    # body = json.loads(request.body)
    if request.method == 'GET' or request.method == 'DELETE':
        body = request.GET
        option = body.get('option', '')
        if option == '00':
            return master_query(request)
        elif option == '12':
            return slave_query(request)
        elif request.method == 'DELETE':
            return slave_delete(request)

    else:
        body = json.loads(request.body)
        option = body.get('option', '')
        if request.method == 'POST':
            return slave_create(request)
        elif request.method == 'PUT':
            if option == '01':
                return master_update(request)
            if option == '11':
                return slave_modify(request)


@csrf_exempt  # POST表单防止跨站请求伪造
@transaction.atomic  # 数据库操作失败回滚
def master_query(request):
    """
    查询请求信息
    """
    # body = json.loads(request.body)
    body = request.GET
    task = body.get('order_id', '')
    # req = list(Request.objects.values().filter(task__exact=task))

    req = Request.objects.filter(task__exact=task)

    # slave = list(i.requester for i in req)

    response_body = [{
        "task_name": each.task.task_name,
        "task_id": each.task.uid,
        "requester_id": each.requester.uid,
        "requester_name": each.requester.user_name,
        "request_status": each.request_status,
        "uid": each.uid,
        "description": each.description
    } for each in req]
    # slave = list
    # for i in req:
    #     slave.append(Profile.objects.values().get(uid=i['uid']))

    if req.exists() == False:
        return HttpResponseBadRequest("没有该任务的申请")
    else:
        return json_response(200, 'OK', response_body)


@csrf_exempt  # POST表单防止跨站请求伪造
@transaction.atomic  # 数据库操作失败回滚
def master_update(request):
    """
    更新召集令请求状态
    """
    body = json.loads(request.body)
    # body = request.GET
    rid = body.get('request_id', '')
    time = body.get('time', '')
    status = body.get('state', None)

    
    try:
        req = Request.objects.get(uid=rid)

        task = req.task

        if status == 'accepted' and task.cur_people < task.max_people :
            task.task_status = Task.FINISHED
            status = Request.AGREE
            # task_success(rid, time)
            task.cur_people += 1
            task.save()
        elif status == 'denied':
            status = Request.REFUSE

        req.request_status = status
        req.save()
    except Exception as e:
        # return json_response(400002, 'Accept Request Error', {'error': str(e)})
        return HttpResponseServerError
    else:
        data = Request.objects.values().get(uid=rid)
        return json_response(200, 'OK', data)
    finally:
        req = Request.objects.get(uid = rid)
        if req.request_status == 1:
            task_success(rid,time)
            



@csrf_exempt
@transaction.atomic  # 数据库操作失败回滚
def task_success(rid, time):
    """
    召集成功写入数据库
    """
    req = Request.objects.get(uid=rid)
    master = req.task.master
    slave = req.requester
    master_cost = 3
    slave_cost = 1
    # complete_date = req.updated_at
    # complete_date = time.strftime('%Y-%m-%d')
    try:
        success = Success.objects.get(request = rid)
    except Success.DoesNotExist:
        try:
            s = Success(
                request=req,
                master=master,
                slave=slave,
                master_cost=master_cost,
                slave_cost=slave_cost,
                complete_date= date.today(),
            )
            s.save()
        except Exception as e:
            return HttpResponseServerError("")
    finally:
        add_income(req, time)


@csrf_exempt
@transaction.atomic  # 数据库操作失败回滚
def add_income(req, time):
    """
    收入统计
    """
    # date = format_date(time)        # 达成日期
    set_date = datetime.today().strftime(r"%Y-%m-%d")         # 达成日期
    # try:
    #     req = Request.objects.get(uid=rid)    # 查询请求
    # except Request.DoesNotExist:
    #     return HttpResponseBadRequest("没有该申请")
    ttype = req.task.task_type       # 召集令类型
    city = req.task.master.city     # 城市
    cost = 4        # 完成一次召集令请求的收入
    # db = MySQLdb.connect("112.74.57.177", "task1",
    #                      "task1", "task1234", charset='utf8')
    # cursor = db.cursor()
    # cursor.execute("select * from server_income where task_type = %s and city = %s and date = %s", 
    #             (ttype, city, set_date))
    # data = cursor.fetchall()
    try:
        income = Income.objects.get(task_type = ttype,city = city)
    except Income.DoesNotExist:
        try:
            Income.objects.create(
                date=date(2020, 12, 7),
                city=city,
                task_type=ttype,
                task_number=1,
                cost=4,
            )
        except Exception as e:
            return HttpResponseBadRequest("创建income表失败")   
    else:
        inc = Income.objects.get(city=city, task_type=ttype, date=set_date)
        inc.task_number += 1
        inc.cost += 4
        inc.save()



@csrf_exempt  # POST表单防止跨站请求伪造
@transaction.atomic  # 数据库操作失败回滚
def slave_create(request):
    """
    接令者申请召集令
    """
    body = json.loads(request.body)
    tid = body.get('order_id', '')
    pid = body.get('slave_id', '')
    desc = body.get('request_msg', '')

    try:
        task = Task.objects.get(uid=tid)
        req = Profile.objects.get(uid=pid)
        name = req.user_name
        if(task.cur_people<task.max_people):
            Request.objects.create(
                task=task,
                requester=req,
                description=desc,
                requester_name=name
            )
        else:
            return HttpResponseBadRequest({"msg":"召集人数已满"})
    except Exception as e:
        # return json_response(400003, 'Create Request Error', {'error': str(e)})
        return HttpResponseServerError
    else:
        data = Request.objects.values().get(
            task=tid, requester=pid)
        return json_response(200, 'OK', data)


@csrf_exempt
@transaction.atomic
def slave_modify(request):
    """
    接令者修改申请信息
    """
    body = json.loads(request.body)
    # body = request.GET
    req = body.get('request_id', '')
    msg = body.get('request_msg', '')
    name = body.get('request_name')

    try:
        r = Request.objects.get(uid=req)
        r.description = msg
        r.save()
    except Exception as e:
        # return json_response(400004, 'Modify Request Error', {'error': str(e)})
        return HttpResponseBadRequest("Bad Request")
    else:
        return json_response(200, 'OK', {"request_name": name, "msg": msg})

@csrf_exempt
@transaction.atomic
def slave_query(request):
    """
    接令人查询已经接受的召集令请求
    """
    # body = json.loads(request.body)
    body = request.GET
    slave = body.get('slave_id', '')
    try:
        requests = list(Request.objects.filter(
            requester__exact=slave))
    except Exception as e:
        # return json_response(400005, 'Slave Query Error', {'error': str(e)})
        return HttpResponseServerError
    else:
        response_body = [{
            "task_name":each.task.task_name,
            "task_id": each.task.uid,
            "requester_id": each.requester.uid,
            "requester_name": each.requester.user_name,
            "request_status": each.request_status,
            "uid": each.uid,
            "description": each.description
        } for each in requests]
        return json_response(200, 'OK', response_body)

@csrf_exempt
@transaction.atomic
def slave_delete(request):
    """
    接令人删除为同意的召集令请求
    """
    # body = json.loads(request.body) 
    body = request.GET
    req = body.get('request_id', '')
    try:
        Request.objects.filter(
            uid__exact=req, request_status__exact=0).delete()
    except Request.DoesNotExist:
        return HttpResponseBadRequest("申请不存在")
    else:
        return json_response(200, 'OK', {})
