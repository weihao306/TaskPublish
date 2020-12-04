from django.http import QueryDict  # 引入QueryDict模块
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


def manage_task(request):
    if request.method == 'GET':
        if request.body == {}:
            all_task(request)
        else:
            query_task(request)
    elif request.method == 'POST':
        create_task(request)
    elif request.method == 'DELETE':
        delete_task(request)
    elif request.method == 'PUT':
        update_task(request)


@csrf_exempt  # POST表单防止跨站请求伪造
@transaction.atomic  # 数据库操作失败回滚
def all_task(request):
    """
    查询所有召集令的信息
    """
    task = Task.objects.filter(status__exact=True)
    data = serializers.serialize('json', task, fields=('updated_at',))
    return json_response(200, 'OK', data)


@csrf_exempt
@transaction.atomic
def query_task(request):
    """
    令主查询自己所有的召集令信息
    """
    master = request.GET.get('uuid', '')
    try:
        task = Task.objects.filter(master__exact=master, status=True)
    except Exception as e:
        return json_response(200001, 'Task Not Found', {'error': str(e)})
    else:
        data = serializers.serialize('json', task, fields=('master', 'updated_at'))
        return json_response(200, 'OK', data)


@csrf_exempt
@transaction.atomic
def create_task(request):
    """
    令主发布召集令
    """
    master = request.POST.get('user_id', '')
    task_type = request.POST.get('task_type', '')
    task_name = request.POST.get('task_name', '')
    description = request.POST.get('description', '')
    cur_people = request.POST.get('cur_people', '')
    max_people = request.POST.get('max_people', '')
    created_at = request.POST.get('start_time', '')
    end_time = request.POST.get('end_time', '')
    task_status = request.POST.get('task_status', '')
    photo = request.POST.get('photo')

    try:
        p = Profile.objects.filter(uid__exact=master)
    except Profile.DoesNotExist:
        return json_response(*UserError.UserNotFound)
    else:
        Task.objects.create(
            master=master,
            task_type=task_type,
            task_name=task_name,
            description=description,
            cur_people=cur_people,
            max_people=max_people,
            created_at=created_at,
            end_time=end_time,
            task_status=task_status,
            photo=photo,
        )
        try:
            task = Task.objects.filter(master__exact=master, created_at__exact=created_at, end_time__exact=end_time,
                                       max_people__exact=max_people)
        except Exception as e:
            return json_response(200002, 'Task Create Error', {'error': str(e)})
        else:
            return json_response(200, 'OK', serializers.serialize('json', task))


@transaction.atomic
def delete_task(request):
    """
    令主删除召集令
    """
    delete = QueryDict(request.body)
    try:
        task = delete.get('order_id', '')
        Task.objects.filter(uid__exact=task).delete()
    except Exception as e:
        return json_response(200003, 'Task Delete Error', {'error': str(e)})
    else:
        return json_response(200, 'OK', {})


@transaction.atomic
def update_task(request):
    """
    更新召集令信息
    """
    put = QueryDict(request.body)
    try:
        tid = put.get('order_id', '')
        task = Task.objects.filter(uid__exact=tid)
    except Task.DoesNotExist:
        return json_response(*TaskError.TaskNotExist)
    else:
        task.task_name = put.get('order_name', '')
        task.task_type = put.get('order_type', '')
        task.description = put.get('order_description', '')
        task.photo = put.get('photo')
        try:
            task.save()
        except Exception as e:
            return json_response(200004, 'Database Update Error', {'error', str(e)})
        else:
            newt = Task.objects.get(uid=tid)
            return json_response(200, 'OK', serializers.serialize('json', newt))










