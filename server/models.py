from django.db import models
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

    UNVERIFIED = 0
    ACTIVATED = 1
    DISABLED = 2
    DELETED = 3
    ASSIGN = 4

    USER_STATUS = (
        (UNVERIFIED, u'未验证'),
        (ACTIVATED, u'已激活'),
        (DISABLED, u'已禁用'),
        (DELETED, u'已删除'),
        (ASSIGN, u'已分配'),
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
    user_type = models.IntegerField(_(u'用户类型'), choices=USER_TYPE, default=GUEST_USER, help_text=u'用户类型', db_index=True)
    user_name = models.CharField(_(u'姓名'), max_length=32, blank=True, null=True, help_text=u'用户姓名', db_index=True)
    phone = models.CharField(_(u'联系电话'), max_length=11, blank=True, null=True, help_text=u'用户电话', db_index=True)
    user_level = models.IntegerField(_(u'用户级别'), choices=USER_LEVEL, default=GENERAL_USER, help_text=u'用户级别',
                                     db_index=True)
    user_status = models.IntegerField(_(u'用户状态'), choices=USER_STATUS, default=ACTIVATED)
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

    uid = models.UUIDField(_(u'召集令标识'), max_length=32, primary_key=True, default=uuid.uuid4, editable=False,
                           help_text=u'召集令唯一标识', db_index=True, unique=True)
    owner_uid = models.CharField(_(u'令主标识'), max_length=32, help_text=u'令主唯一标识', db_index=True, unique=True)
    task_type = models.IntegerField(_(u'召集令类型'), default=TECHNICAL, choices=TASK_TYPE, help_text=u'召集令类型', db_index=True)
    task_name = models.CharField(_(u'召集令名称'), max_length=32, blank=True, null=True, help_text=u'召集令名称', db_index=True)
    describe = models.TextField(_(u'召集令描述'), max_length=200, blank=True, null=True, help_text=u'召集令描述')
    people_number = models.IntegerField(_(u'召集人数'), default=1, help_text=u'召集人数')
    end_time = models.DateTimeField(_(u'结束日期'), null=True, blank=True, help_text=u'结束日期')

