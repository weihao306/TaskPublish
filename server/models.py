import os

from django.db import models
from django.db.models import DO_NOTHING, CASCADE
from django.utils.translation import ugettext_lazy as _
from utils.basemodels import CreateUpdateMixin
import uuid


# Create your models here.

class Profile(CreateUpdateMixin):
    """
    用户信息类
    """
    ADMIN_USER = 0
    GUEST_USER = 1

    USER_TYPE = (
        (GUEST_USER, u'普通用户'),
        (ADMIN_USER, u'管理员')
    )

    DIAMOND_USER = 0
    IMPORTANT_USER = 1
    GENERAL_USER = 2

    USER_LEVEL = (
        (DIAMOND_USER, u'钻石用户'),
        (IMPORTANT_USER, u'重要用户'),
        (GENERAL_USER, u'一般用户')
    )

    IDENTIFICATION_CARD = 0
    PASSPORT = 1

    CERTIFICATES = (
        (IDENTIFICATION_CARD, u'居民身份证'),
        (PASSPORT, u'护照')
    )

    uid = models.UUIDField(_(u'用户标识'), max_length=32, primary_key=True, default=uuid.uuid4, editable=False,
                           help_text=u'用户唯一标识', db_index=True, unique=True)
    account = models.CharField(_(u'用户名'), max_length=32, help_text=u'用户名', db_index=True, unique=True)
    password = models.CharField(_(u'登录密码'), max_length=32, help_text=u'登录密码')
    user_type = models.IntegerField(_(u'用户类型'), choices=USER_TYPE, default=GUEST_USER, help_text=u'用户类型')
    user_name = models.CharField(_(u'姓名'), max_length=32, blank=True, null=True, help_text=u'用户姓名')
    phone = models.CharField(_(u'联系电话'), max_length=11, blank=True, null=True, help_text=u'用户电话')
    user_level = models.IntegerField(_(u'用户级别'), choices=USER_LEVEL, default=GENERAL_USER, help_text=u'用户级别',
                                     db_index=True)
    introduction = models.TextField(_(u'用户简介'), max_length=200, blank=True, null=True, help_text=u'用户简介')
    city = models.CharField(_(u'注册城市'), max_length=32, blank=True, null=True, help_text=u'用户城市')
    cert_type = models.IntegerField(_(u'证件类型'), choices=CERTIFICATES, default=IDENTIFICATION_CARD, help_text=u'证件类型',
                                    blank=True)
    cert_number = models.CharField(_(u'证件号码'), max_length=32, blank=True, null=True, help_text=u'证件号码')

    def __str__(self):
        return str(self.account)

    @property
    def data(self):
        return {
            'uid': self.uid,
            'account': self.account,
            'name': self.user_name or ''
        }


def user_directory_path(instance, filename):
    ext = filename.split('.').pop()
    filename = '{0}.{1}'.format(instance.task_name, ext)
    return os.path.join(str(instance.TASK_TYPE[instance.task_type][1]), filename)  # 系统路径分隔符差异，增强代码重用性


class Task(CreateUpdateMixin):
    """
    召集令信息
    """
    TECHNICAL = 0
    ACADEMIC = 1
    PRACTICE = 2
    VOLUNTEER = 3
    PLAY = 4

    TASK_TYPE = (
        (TECHNICAL, u'技术交流'),
        (ACADEMIC, u'学术探讨'),
        (PRACTICE, u'社会实践'),
        (VOLUNTEER, u'公益志愿者'),
        (PLAY, u'游玩'),
    )

    FINISHED = 0
    WAITING = 1
    CANCELLED = 2
    OVERDUE = 3

    TASK_STATUS = (
        (FINISHED, u'已完成'),
        (WAITING, u'待响应'),
        (CANCELLED, u'已取消'),
        (OVERDUE, u'已逾期'),
    )

    uid = models.UUIDField(_(u'召集令标识'), max_length=32, primary_key=True, default=uuid.uuid4, editable=False,
                           help_text=u'召集令唯一标识', db_index=True, unique=True)
    master = models.OneToOneField(to='Profile', to_field='uid', on_delete=CASCADE, help_text=u'令主',
                                  verbose_name=_(u'令主'))
    task_type = models.IntegerField(_(u'召集令类型'), default=TECHNICAL, choices=TASK_TYPE, help_text=u'召集令类型')
    task_name = models.CharField(_(u'召集令名称'), max_length=32, blank=True, null=True, help_text=u'召集令名称')
    description = models.TextField(_(u'召集令描述'), max_length=200, blank=True, null=True, help_text=u'召集令描述')
    cur_people = models.IntegerField(_(u'当前召集人数'), help_text=u'当前召集人数')
    max_people = models.IntegerField(_(u'最大召集人数'), help_text=u'最大召集人数')
    end_time = models.DateTimeField(_(u'结束日期'), null=True, blank=True, help_text=u'结束日期')
    task_status = models.IntegerField(_(u'召集令状态'), default=WAITING, choices=TASK_STATUS, help_text=u'召集令状态')
    photo = models.ImageField(_(u'介绍图片'), upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return str(self.task_name)

    # 当用户没有上传照片，模板中调用 [ModelName].[ImageFieldName].url 时赋予一个默认路径
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return '/media/default/task.jpg'


class Request(CreateUpdateMixin):
    """
    请求召集令关系表
    """
    PENDING = 0
    AGREE = 1
    REFUSE = 2
    CANCELLED = 3

    REQUEST_STATUS = (
        (PENDING, u'待处理'),
        (AGREE, u'同意'),
        (REFUSE, u'拒绝'),
        (CANCELLED, u'取消'),
    )

    uid = models.UUIDField(_(u'请求标识'), max_length=32, primary_key=True, default=uuid.uuid4, editable=False,
                           help_text=u'请求标识', db_index=True, unique=True)
    task = models.OneToOneField(to='Task', to_field='uid', on_delete=CASCADE, verbose_name=u'召集令', help_text=u'召集令')
    requester = models.OneToOneField(to='Profile', to_field='uid', on_delete=CASCADE, verbose_name=u'请求者', help_text=u'请求者')
    description = models.TextField(_(u'请求描述'), max_length=200, blank=True, null=True, help_text=u'请求描述')
    request_status = models.IntegerField(_(u'请求状态'), default=PENDING, choices=REQUEST_STATUS, help_text=u'请求状态')

    def __str__(self):
        return str(self.pk)


class Success(CreateUpdateMixin):
    """
    召集令成功明细表
    """
    uid = models.UUIDField(_(u'召集成功标识'), max_length=32, primary_key=True, default=uuid.uuid4, editable=False,
                           help_text=u'召集成功标识', db_index=True, unique=True)
    request = models.OneToOneField(to='Request', to_field='uid', on_delete=CASCADE, verbose_name=u'请求标识', help_text=u'请求标识')
    master = models.CharField(_(u'令主标识'), max_length=32, blank=False, help_text=u'令主标识')
    slave = models.CharField(_(u'接令用户标识'), max_length=32, blank=False, help_text=u'接令用户标识')
    master_cost = models.IntegerField(_(u'令主支付费用'), help_text=u'令主支付费用')
    slave_cost = models.IntegerField(_(u'接令用户支付费用'), help_text=u'接令用户支付费用')
    complete_date = models.DateTimeField(_(u'达成日期'), blank=False, help_text=u'达成日期')


# class Slave(Success):
#     """
#     成功明细表附表，用于保存请求者相关信息
#     """
#     request = models.ForeignKey(to='Request', to_field='uid', on_delete=CASCADE, verbose_name=u'请求标识',
#                                 help_text=u'请求标识')
#     slave_id = models.CharField(_(u'请求用户标识'), max_length=32, null=True, blank=False, help_text=u'请求用户标识')
#     slave_cost = models.IntegerField(_(u'接令支付费用'), default=0, help_text=u'接令支付费用')
#
#
# class Master(Success):
#     """
#     成功明细表附表，用于保存令主相关信息
#     """
#     master_id = models.CharField(_(u'令主标识'), max_length=32, null=True, blank=False, help_text=u'令主标识')
#     master_cost = models.IntegerField(_(u'令主支付费用'), default=0, help_text=u'令主支付费用')


class Income(CreateUpdateMixin):
    """
    中介收益汇总表
    """
    TECHNICAL = 0
    ACADEMIC = 1
    PRACTICE = 2
    VOLUNTEER = 3
    PLAY = 4

    TASK_TYPE = (
        (TECHNICAL, u'技术交流'),
        (ACADEMIC, u'学术探讨'),
        (PRACTICE, u'社会实践'),
        (VOLUNTEER, u'公益志愿者'),
        (PLAY, u'游玩'),
    )

    uid = models.UUIDField(_(u'收入明细标识'), max_length=32, primary_key=True, default=uuid.uuid4, editable=False,
                           help_text=u'收入明细标识', db_index=True, unique=True)
    date = models.DateTimeField(_(u'日期'), db_index=True, help_text=u'日期', unique=True)
    city = models.CharField(_(u'地域'), max_length=32, null=True, help_text=u'地域')
    task_type = models.IntegerField(_(u'召集令类型'), default=TECHNICAL, blank=False, choices=TASK_TYPE, db_index=True,
                                    help_text=u'召集令类型')
    task_number = models.IntegerField(_(u'达成次数'), help_text=u'达成次数')
    cost = models.IntegerField(_(u'收入'), help_text=u'收入')

    def __str__(self):
        return str(self.pk)
