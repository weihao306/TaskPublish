import os

from django.db import models
from django.utils.translation import ugettext_lazy as _


class CreateUpdateMixin(models.Model):
    # 表明项目是否可用
    # status = models.BooleanField(_(u'状态'), default=True, help_text=u'状态', db_index=True)
    # 用户注册时间/召集令创建时间
    created_at = models.DateTimeField(_(u'创建时间'), auto_now_add=True, editable=True, help_text=_(u'创建时间'))
    # 用户/召集令修改时间
    updated_at = models.DateTimeField(_(u'更新时间'), auto_now=True, editable=True, help_text=_(u'更新时间'))

    class Meta:
        abstract = True
