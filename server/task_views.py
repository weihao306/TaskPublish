from datetime import date, datetime, timezone
from django.http import QueryDict
from django.http.response import Http404  # 引入QueryDict模块
from django.shortcuts import render
from furl import furl  # 引入furl模块
from django.db import transaction  # 引入数据库事务模块
from django.shortcuts import redirect  # 引入重定向方法
from django.views.decorators.csrf import csrf_exempt  # 引入防跨站请求伪造装饰器
from django.conf import settings  # 项目配置模块
from io import BytesIO  # 流传输模块
from utils.response import json_response  # 引入响应对象
from server.models import Task, Profile  # 引入数据模型
from django.core import serializers  # 引入序列化方法
import json


@csrf_exempt  # POST表单防止跨站请求伪造
def manage_task(request):
    if request.method == 'GET':
        body = request.GET
        if body.get('all', None) != None:
            return all_task(request)
        else:
            return query_task(request)
    elif request.method == 'POST':
        return create_task(request)
    elif request.method == 'DELETE':
        return delete_task(request)
    elif request.method == 'PUT':
        return update_task(request)


@csrf_exempt  # POST表单防止跨站请求伪造
@transaction.atomic  # 数据库操作失败回滚
def all_task(request):
    """
    查询所有召集令的信息
    """
    task = list(Task.objects.values().all())
    # data = serializers.serialize('json', task, fields=('updated_at',))
    return json_response(200, 'OK', task)


@csrf_exempt
@transaction.atomic
def query_task(request):
    """
    令主查询自己所有的召集令信息
    """
    # body = json.loads(request.body)
    body = request.GET
    master = body.get('master_id', '')
    try:
        task = list(Task.objects.values().filter(master__exact=master))
    except Exception as e:
        return json_response(200001, 'Task Not Found', {'error': str(e)})
    else:
        # data = serializers.serialize(
        #     'json', task, fields=('master', 'updated_at'))
        return json_response(200, 'OK', task)


@csrf_exempt
@transaction.atomic
def create_task(request):
    """
    令主发布召集令
    """
    body = json.loads(request.body)
    master = body.get('master_id', '')
    task_type = body.get('task_type', None)
    task_name = body.get('task_name', '')
    description = body.get('description', '')
    cur_people = body.get('cur_people', 0)
    max_people = body.get('max_people', 0)
    start_time = body.get('start_time', date.today())
    end_time = body.get('end_time',date.today())
    task_status = 1
    photo = body.get('photos',None)

    try:
        p = Profile.objects.get(uid=master)
    except Profile.DoesNotExist:
        raise Http404
        # json_response(200001, 'User Not Found', {})
    else:
        Task.objects.create(
            master=p,
            task_type=task_type,
            task_name=task_name,
            description=description,
            cur_people=cur_people,
            max_people=max_people,
            start_time=start_time,
            end_time=end_time,
            task_status=task_status,
            photo=photo,
        )
        try:
            task = Task.objects.filter(master__exact=master, created_at__exact=created_at, end_time__exact=end_time,
                                       max_people__exact=max_people).values()
        except Exception as e:
            return json_response(200002, 'Task Create Error', {'error': str(e)})
        else:
            return json_response(200, 'OK', serializers.serialize('json', task))


@transaction.atomic
def delete_task(request):
    """
    令主删除召集令
    """
    body = json.loads(request.body)
    # body = request.GET
    try:
        task = body.get('order_id', '')
        Task.objects.get(uid=task).delete()
    except Exception as e:
        return json_response(200003, 'Task Delete Error', {'error': str(e)})
    else:
        return json_response(200, 'OK', {})


@transaction.atomic
def update_task(request):
    """
    更新召集令信息
    """
    body = json.loads(request.body)
    # body = request.GET
    try:
        tid = body.get('order_id', '')
        task = Task.objects.filter(uid__exact=tid)
    except Task.DoesNotExist:
        return json_response(200001, 'Task Not Found', {})
    else:
        task.task_name = body.get('order_name', '')
        task.task_type = body.get('order_type', '')
        task.description = body.get('order_description', '')
        if body.get('photo', None) != None:
            task.photo = body.get('photo')

        try:
            task.save()
        except Exception as e:
            return json_response(200004, 'Database Update Error', {'error', str(e)})
        else:
            newt = Task.objects.get(uid=tid)
            return json_response(200, 'OK', serializers.serialize('json', newt))
