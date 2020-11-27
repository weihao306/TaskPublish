from django.contrib import admin
from server.models import Profile, Task, Request


# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    用户信息后台配置
    """
    list_display = ('uid', 'user_type', 'account', 'user_level', 'user_name',
                    'phone', 'city', 'cert_type', 'cert_number', 'introduction')
    list_filter = ('user_level', 'user_type')
    search_fields = ('account', 'user_name')
    readonly_fields = ('uid',)
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        obj.save()

    def delete_model(self, request, obj):
        obj.delete()


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    召集令信息后台管理
    """
    list_display = ('uid', 'master', 'task_type', 'task_status', 'task_name',
                    'description', 'cur_people', 'max_people', 'end_time')
    list_filter = ('task_status', 'task_type')
    search_fields = ('task_name',)
    readonly_fields = ('uid',)
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        obj.save()

    def delete_model(self, request, obj):
        obj.delete()


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    """
    召集令请求管理
    """
    list_display = ('uid', 'task', 'requester', 'description', 'request_status')
    readonly_fields = ('uid',)
    search_fields = ('create_at', 'update_at')
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        obj.save()

    def delete_model(self, request, obj):
        obj.delete()